"""
Firebase (Firestore & Realtime Database) Centralized Database Module for Phishy & ThreatLens Platform.
Provides unified persistent storage for:
- User authentication and profile management
- Simulation click logs
- Email tracking (pixel opens)
- Flagged email threat intelligence reports

Supports production Firebase Realtime Database and Cloud Firestore via firebase-admin SDK,
as well as local persistence fallback store.
"""

import os
import json
import uuid
import logging
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Union
import bcrypt
import jwt
import pandas as pd

logger = logging.getLogger(__name__)

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOCAL_DB_FILE = DATA_DIR / "firestore_local.json"

# Load environment variables if not yet loaded
try:
    from dotenv import load_dotenv
    if (BASE_DIR.parent / ".env").exists():
        load_dotenv(BASE_DIR.parent / ".env")
    elif (BASE_DIR / ".env").exists():
        load_dotenv(BASE_DIR / ".env")
    else:
        load_dotenv()
except ImportError:
    pass

# Configuration
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", os.getenv("GCP_PROJECT", "phishy-app-f5891"))
FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "https://phishy-app-f5891-default-rtdb.firebaseio.com/")

JWT_SECRET = os.getenv("JWT_SECRET", "phishy-jwt-secret-key-threatlens-2024-secure")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))

# Global references
_firebase_initialized = False
_firestore_client = None
_rtdb_enabled = False
_db_lock = threading.RLock()


# ==============================================================================
# Password Hashing & JWT Security Utilities
# ==============================================================================

def hash_password(password: str) -> str:
    """Hash password using bcrypt with automatic salt generation"""
    pw_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored bcrypt or legacy salt hash"""
    try:
        pw_bytes = password.encode("utf-8")
        if stored_hash.startswith(("$2b$", "$2a$", "$2y$")):
            return bcrypt.checkpw(pw_bytes, stored_hash.encode("utf-8"))
        if "$" in stored_hash:
            import hashlib
            salt, hex_hash = stored_hash.split("$", 1)
            salted = f"{salt}:{password}".encode("utf-8")
            return hashlib.sha256(salted).hexdigest() == hex_hash
        import hashlib
        return hashlib.sha256(pw_bytes).hexdigest() == stored_hash
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create signed JWT access token with expiration"""
    to_encode = data.copy()
    now_utc = datetime.now(timezone.utc)
    if expires_delta:
        expire = now_utc + expires_delta
    else:
        expire = now_utc + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire, "iat": now_utc})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_access_token(token: str) -> Optional[dict]:
    """Verify and decode signed JWT access token"""
    try:
        if token.startswith("Bearer "):
            token = token[7:].strip()
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception as e:
        logger.debug(f"JWT verification failed: {e}")
        return None


# ==============================================================================
# Local Firestore Storage Engine (Zero-Config Fallback & Offline Development)
# ==============================================================================

class LocalFirestoreStore:
    """
    Thread-safe local persistence store replicating Firestore/RTDB collection/document
    structure in JSON format for offline development or testing.
    """
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.lock = threading.RLock()
        self.data: Dict[str, Dict[str, Any]] = {
            "users": {},
            "click_logs": {},
            "email_opens": {},
            "flagged_emails": {}
        }
        self.load()

    def load(self):
        with self.lock:
            if self.filepath.exists():
                try:
                    with open(self.filepath, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        for col in ["users", "click_logs", "email_opens", "flagged_emails"]:
                            if col in loaded and isinstance(loaded[col], dict):
                                self.data[col] = loaded[col]
                except Exception as e:
                    logger.error(f"Error loading local Firestore database file: {e}")

    def save(self):
        with self.lock:
            try:
                temp_file = self.filepath.with_suffix(".tmp")
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=2, default=str)
                temp_file.replace(self.filepath)
            except Exception as e:
                logger.error(f"Error saving local Firestore database file: {e}")

    def set_doc(self, collection: str, doc_id: str, data: dict):
        with self.lock:
            if collection not in self.data:
                self.data[collection] = {}
            doc_data = data.copy()
            doc_data["id"] = doc_id
            self.data[collection][doc_id] = doc_data
            self.save()

    def get_doc(self, collection: str, doc_id: str) -> Optional[dict]:
        with self.lock:
            return self.data.get(collection, {}).get(doc_id)

    def delete_doc(self, collection: str, doc_id: str) -> bool:
        with self.lock:
            if collection in self.data and doc_id in self.data[collection]:
                del self.data[collection][doc_id]
                self.save()
                return True
            return False

    def list_docs(self, collection: str) -> List[dict]:
        with self.lock:
            return list(self.data.get(collection, {}).values())


_local_store = LocalFirestoreStore(LOCAL_DB_FILE)


# ==============================================================================
# Firebase Initialization
# ==============================================================================

def init_firebase() -> bool:
    """Initialize Firebase Admin SDK (Cloud Firestore & Realtime Database)"""
    global _firebase_initialized, _firestore_client, _rtdb_enabled
    with _db_lock:
        if _firebase_initialized:
            return True

        import firebase_admin
        from firebase_admin import credentials, firestore, db

        raw_json_env = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "").strip()
        key_str = FIREBASE_SERVICE_ACCOUNT_KEY.strip() if FIREBASE_SERVICE_ACCOUNT_KEY else ""

        key_path = None
        key_dict = None

        if raw_json_env:
            try:
                key_dict = json.loads(raw_json_env)
            except Exception as e:
                logger.error(f"Error parsing FIREBASE_SERVICE_ACCOUNT_JSON: {e}")
        elif key_str.startswith("{"):
            try:
                key_dict = json.loads(key_str)
            except Exception as e:
                logger.error(f"Error parsing FIREBASE_SERVICE_ACCOUNT_KEY as JSON: {e}")
        elif key_str:
            p = Path(key_str)
            if p.exists():
                key_path = p

        if not key_dict and not key_path:
            for candidate in [
                BASE_DIR.parent / "service-account.json",
                BASE_DIR / "service-account.json",
                BASE_DIR.parent / "firebase-service-account.json"
            ]:
                if candidate.exists():
                    key_path = candidate
                    break

        app_initialized = False

        if firebase_admin._apps:
            app_initialized = True
            logger.info("Connected to existing Firebase Admin app")
        elif key_dict:
            try:
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred, {
                    "projectId": FIREBASE_PROJECT_ID,
                    "databaseURL": FIREBASE_DATABASE_URL or None
                })
                app_initialized = True
                logger.info("Firebase Admin initialized using JSON environment variable")
            except Exception as e:
                logger.error(f"Error initializing Firebase from JSON dictionary: {e}")
        elif key_path and key_path.exists():
            try:
                cred = credentials.Certificate(str(key_path))
                firebase_admin.initialize_app(cred, {
                    "projectId": FIREBASE_PROJECT_ID,
                    "databaseURL": FIREBASE_DATABASE_URL or None
                })
                app_initialized = True
                logger.info(f"Firebase Admin initialized with key file: {key_path}")
            except Exception as e:
                logger.error(f"Error initializing Firebase with key {key_path}: {e}")
        elif os.getenv("FIRESTORE_EMULATOR_HOST"):
            try:
                firebase_admin.initialize_app(options={"projectId": FIREBASE_PROJECT_ID})
                app_initialized = True
                logger.info("Connected to Firestore Emulator")
            except Exception as e:
                logger.warning(f"Error connecting to Firestore Emulator: {e}")
        elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and Path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")).exists():
            try:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    "projectId": FIREBASE_PROJECT_ID,
                    "databaseURL": FIREBASE_DATABASE_URL or None
                })
                app_initialized = True
                logger.info("Firebase Admin initialized using Application Default Credentials")
            except Exception as e:
                logger.warning(f"Error initializing ADC: {e}")

        if app_initialized:
            # 1. Probe Realtime Database
            if FIREBASE_DATABASE_URL:
                try:
                    db.reference("/").get()
                    _rtdb_enabled = True
                    logger.info(f"Connected to Firebase Realtime Database ({FIREBASE_DATABASE_URL})")
                except Exception as e:
                    logger.warning(f"Could not connect to Realtime Database: {e}")
                    _rtdb_enabled = False

            # 2. Probe Cloud Firestore
            try:
                client = firestore.client()
                list(client.collections())
                _firestore_client = client
                logger.info(f"Connected to Cloud Firestore (project: {FIREBASE_PROJECT_ID})")
            except Exception as e:
                logger.info(f"Cloud Firestore probe note: {e}")
                _firestore_client = None

        _firebase_initialized = True
        return True


def get_db():
    """Returns Firestore client if available, else None"""
    global _firestore_client
    if not _firebase_initialized:
        init_firebase()
    return _firestore_client


def is_live_firebase() -> bool:
    """Returns True if connected to live Cloud Firestore or Realtime Database"""
    return (_firestore_client is not None) or _rtdb_enabled


def get_firebase_mode() -> str:
    """Returns human-readable Firebase active database mode"""
    if _firestore_client is not None and _rtdb_enabled:
        return "Live Cloud Firestore & Realtime Database"
    elif _firestore_client is not None:
        return "Live Cloud Firestore"
    elif _rtdb_enabled:
        return "Live Firebase Realtime Database"
    else:
        return "Local Firestore Engine"


# ==============================================================================
# Unified Cloud & Local Synchronization Layer
# ==============================================================================

def _sync_set_doc(collection: str, doc_id: str, data: dict):
    """Write document to Realtime Database, Firestore, and local store"""
    # 1. Realtime Database
    if _rtdb_enabled:
        try:
            from firebase_admin import db
            db.reference(f"/{collection}/{doc_id}").set(data)
        except Exception as e:
            logger.error(f"Error writing {collection}/{doc_id} to Realtime DB: {e}")

    # 2. Firestore
    if _firestore_client:
        try:
            _firestore_client.collection(collection).document(doc_id).set(data)
        except Exception as e:
            logger.error(f"Error writing {collection}/{doc_id} to Firestore: {e}")

    # 3. Local store
    _local_store.set_doc(collection, doc_id, data)


def _sync_delete_doc(collection: str, doc_id: str) -> bool:
    """Delete document from Realtime Database, Firestore, and local store"""
    deleted = False
    if _rtdb_enabled:
        try:
            from firebase_admin import db
            db.reference(f"/{collection}/{doc_id}").delete()
            deleted = True
        except Exception as e:
            logger.error(f"Error deleting {collection}/{doc_id} from Realtime DB: {e}")

    if _firestore_client:
        try:
            _firestore_client.collection(collection).document(doc_id).delete()
            deleted = True
        except Exception as e:
            logger.error(f"Error deleting {collection}/{doc_id} from Firestore: {e}")

    local_del = _local_store.delete_doc(collection, doc_id)
    return deleted or local_del


def _sync_get_doc(collection: str, doc_id: str) -> Optional[dict]:
    """Get single document from Firestore, Realtime Database, or local store"""
    if _firestore_client:
        try:
            doc = _firestore_client.collection(collection).document(doc_id).get()
            if doc.exists:
                d = doc.to_dict()
                d["id"] = doc.id
                return d
        except Exception as e:
            logger.error(f"Firestore get error: {e}")

    if _rtdb_enabled:
        try:
            from firebase_admin import db
            data = db.reference(f"/{collection}/{doc_id}").get()
            if data and isinstance(data, dict):
                data["id"] = doc_id
                return data
        except Exception as e:
            logger.error(f"RTDB get error: {e}")

    return _local_store.get_doc(collection, doc_id)


def _sync_list_docs(collection: str) -> List[dict]:
    """List all documents from Firestore, Realtime Database, or local store"""
    if _firestore_client:
        try:
            docs = []
            for doc in _firestore_client.collection(collection).stream():
                d = doc.to_dict()
                d["id"] = doc.id
                docs.append(d)
            if docs:
                return docs
        except Exception as e:
            logger.error(f"Firestore list error: {e}")

    if _rtdb_enabled:
        try:
            from firebase_admin import db
            val = db.reference(f"/{collection}").get()
            if val and isinstance(val, dict):
                docs = []
                for k, v in val.items():
                    if isinstance(v, dict):
                        row = v.copy()
                        row["id"] = k
                        docs.append(row)
                return docs
        except Exception as e:
            logger.error(f"RTDB list error: {e}")

    return _local_store.list_docs(collection)


# ==============================================================================
# Initial Seeding & Synchronization
# ==============================================================================

def init_db():
    """Initialize database, create collections, seed initial users, and migrate CSVs"""
    init_firebase()

    now = datetime.now(timezone.utc).isoformat()
    default_users = [
        ("admin@phishy.local", hash_password("admin123"), "System Administrator", "admin"),
        ("admin@threatlens.local", hash_password("admin123"), "ThreatLens Administrator", "admin"),
        ("john.doe@company.com", hash_password("password123"), "John Doe", "user"),
        ("jane.smith@company.com", hash_password("password123"), "Jane Smith", "user"),
        ("alex.security@company.com", hash_password("password123"), "Alex Security Analyst", "analyst")
    ]

    # Sync local data collections to Realtime Database if RTDB is active
    if _rtdb_enabled:
        try:
            from firebase_admin import db
            rtdb_users = db.reference("/users").get() or {}
            existing_emails = {
                v.get("email", "").lower(): k
                for k, v in rtdb_users.items()
                if isinstance(v, dict) and "email" in v
            }
            # Sync any local users missing in RTDB
            for u in _local_store.list_docs("users"):
                u_email = u.get("email", "").lower()
                if u_email and u_email not in existing_emails:
                    db.reference(f"/users/{u['id']}").set(u)
                    existing_emails[u_email] = u["id"]

            for col in ["click_logs", "email_opens", "flagged_emails"]:
                rtdb_col = db.reference(f"/{col}").get()
                if not rtdb_col:
                    local_items = _local_store.list_docs(col)
                    if local_items:
                        logger.info(f"Syncing {len(local_items)} local records for '{col}' into Firebase Realtime Database...")
                        for item in local_items:
                            if "id" in item:
                                db.reference(f"/{col}/{item['id']}").set(item)
        except Exception as e:
            logger.error(f"Error syncing to RTDB: {e}")

    for email, pw_hash, full_name, role in default_users:
        existing = db_get_user_by_email(email)
        if not existing:
            db_create_user(email=email, password_hash=pw_hash, full_name=full_name, role=role, created_at=now)
        elif not existing.get("password_hash"):
            existing["password_hash"] = pw_hash
            existing["full_name"] = existing.get("full_name") or full_name
            existing["role"] = existing.get("role") or role
            existing["created_at"] = existing.get("created_at") or now
            existing["is_active"] = True
            _sync_set_doc("users", existing["id"], existing)

    # Migrate any legacy CSV files
    migrate_csv_data()
    logger.info(f"Firebase Database ready in mode: {get_firebase_mode()}")


def db_clear_click_logs() -> bool:
    """Clear all click tracking logs in RTDB, Firestore, and local store"""
    if _rtdb_enabled:
        try:
            from firebase_admin import db
            db.reference("/click_logs").delete()
        except Exception as e:
            logger.error(f"Error clearing click_logs in RTDB: {e}")
    if _firestore_client:
        try:
            for doc in _firestore_client.collection("click_logs").stream():
                doc.reference.delete()
        except Exception as e:
            logger.error(f"Error clearing click_logs in Firestore: {e}")
    with _local_store.lock:
        _local_store.data["click_logs"] = {}
        _local_store.save()
    return True


def db_clear_email_opens() -> bool:
    """Clear all email open tracking logs in RTDB, Firestore, and local store"""
    if _rtdb_enabled:
        try:
            from firebase_admin import db
            db.reference("/email_opens").delete()
        except Exception as e:
            logger.error(f"Error clearing email_opens in RTDB: {e}")
    if _firestore_client:
        try:
            for doc in _firestore_client.collection("email_opens").stream():
                doc.reference.delete()
        except Exception as e:
            logger.error(f"Error clearing email_opens in Firestore: {e}")
    with _local_store.lock:
        _local_store.data["email_opens"] = {}
        _local_store.save()
    return True


def db_clear_flagged_emails() -> bool:
    """Clear all flagged email reports in RTDB, Firestore, and local store"""
    if _rtdb_enabled:
        try:
            from firebase_admin import db
            db.reference("/flagged_emails").delete()
        except Exception as e:
            logger.error(f"Error clearing flagged_emails in RTDB: {e}")
    if _firestore_client:
        try:
            for doc in _firestore_client.collection("flagged_emails").stream():
                doc.reference.delete()
        except Exception as e:
            logger.error(f"Error clearing flagged_emails in Firestore: {e}")
    with _local_store.lock:
        _local_store.data["flagged_emails"] = {}
        _local_store.save()
    return True


def migrate_csv_data():
    """Migrate legacy CSV records into Firebase collections if collections are empty"""
    import csv

    # Click logs CSV
    click_csv = DATA_DIR / "click_logs.csv"
    if click_csv.exists() and len(db_get_click_logs(limit=1)) == 0:
        try:
            with open(click_csv, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 4:
                        ts = row[0]
                        email = row[1]
                        action = row[2]
                        ip = row[3]
                        agent = row[4] if len(row) > 4 else None
                        ref = row[5] if len(row) > 5 else None
                        db_add_click_log(email, action, ip, agent, ref, timestamp=ts)
            logger.info("Migrated click_logs.csv into Firebase")
        except Exception as e:
            logger.error(f"Error migrating click_logs CSV: {e}")

    # Email opens CSV
    opens_csv = DATA_DIR / "email_opens.csv"
    if opens_csv.exists() and len(db_get_email_opens(limit=1)) == 0:
        try:
            with open(opens_csv, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 4:
                        ts = row[0]
                        email = row[1]
                        action = row[2]
                        ip = row[3]
                        agent = row[4] if len(row) > 4 else None
                        camp = row[5] if len(row) > 5 else None
                        db_add_email_open(email, action, ip, agent, camp, timestamp=ts)
            logger.info("Migrated email_opens.csv into Firebase")
        except Exception as e:
            logger.error(f"Error migrating email_opens CSV: {e}")


# ==============================================================================
# User Management Operations
# ==============================================================================

def db_get_user_by_email(email: str) -> Optional[dict]:
    """Retrieve user document by email (case-insensitive)"""
    email_clean = email.strip().lower()

    if _firestore_client:
        try:
            docs = _firestore_client.collection("users").where("email", "==", email_clean).limit(1).stream()
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                return data
        except Exception as e:
            logger.error(f"Firestore error fetching user by email {email_clean}: {e}")

    if _rtdb_enabled:
        try:
            from firebase_admin import db
            val = db.reference("/users").get()
            if val and isinstance(val, dict):
                for k, v in val.items():
                    if isinstance(v, dict) and v.get("email", "").lower() == email_clean:
                        doc = v.copy()
                        doc["id"] = k
                        return doc
        except Exception as e:
            logger.error(f"RTDB error fetching user by email {email_clean}: {e}")

    for doc in _local_store.list_docs("users"):
        if doc.get("email", "").lower() == email_clean:
            return doc

    return None


def db_get_user_by_id(user_id: Union[str, int]) -> Optional[dict]:
    """Retrieve user document by ID"""
    return _sync_get_doc("users", str(user_id))


def db_create_user(email: str, password_hash: str, full_name: Optional[str] = None, role: str = "user", created_at: Optional[str] = None) -> dict:
    """Create a new user document in Firebase"""
    email_clean = email.strip().lower()
    now = created_at or datetime.now(timezone.utc).isoformat()
    user_id = str(uuid.uuid4().hex[:12])
    
    user_data = {
        "id": user_id,
        "email": email_clean,
        "password_hash": password_hash,
        "full_name": full_name or email_clean.split("@")[0].capitalize(),
        "role": role or "user",
        "created_at": now,
        "last_login": now,
        "is_active": True
    }

    _sync_set_doc("users", user_id, user_data)
    logger.info(f"Created user {email_clean} in Firebase (ID: {user_id})")
    return user_data


def db_update_user_login(user_id: Union[str, int], last_login: Optional[str] = None) -> bool:
    """Update user's last_login timestamp"""
    uid_str = str(user_id)
    now = last_login or datetime.now(timezone.utc).isoformat()
    user = _sync_get_doc("users", uid_str)
    if user:
        user["last_login"] = now
        _sync_set_doc("users", uid_str, user)
        return True
    return False


def db_update_user_password(user_id: Union[str, int], password_hash: str) -> bool:
    """Update user's password hash in Firebase database"""
    uid_str = str(user_id)
    user = _sync_get_doc("users", uid_str)
    if user:
        user["password_hash"] = password_hash
        _sync_set_doc("users", uid_str, user)
        logger.info(f"Updated password for user {uid_str} in Firebase DB")
        return True
    return False


def db_get_all_users() -> List[dict]:
    """Retrieve all users stored in Firebase"""
    users = _sync_list_docs("users")
    return sorted(users, key=lambda x: str(x.get("created_at", "")))


def db_delete_user(user_id: Union[str, int]) -> bool:
    """Delete a user document from Firebase"""
    return _sync_delete_doc("users", str(user_id))


# ==============================================================================
# Click Logs Operations
# ==============================================================================

def db_add_click_log(user_email: str, action_id: str, ip_address: str, user_agent: Optional[str] = None, referer: Optional[str] = None, timestamp: Optional[str] = None) -> str:
    """Insert click event into Firebase collection"""
    now = timestamp or datetime.now(timezone.utc).isoformat()
    log_id = f"click_{int(datetime.now(timezone.utc).timestamp()*1000)}_{uuid.uuid4().hex[:6]}"
    log_data = {
        "id": log_id,
        "timestamp": now,
        "user_email": user_email.strip().lower(),
        "action_id": action_id,
        "ip_address": ip_address,
        "user_agent": user_agent or "Unknown",
        "referer": referer or ""
    }

    _sync_set_doc("click_logs", log_id, log_data)
    return log_id


def db_get_click_logs(limit: int = 100, user_email: Optional[str] = None, action_id: Optional[str] = None, days: Optional[int] = None) -> List[dict]:
    """Retrieve click logs with optional filtering and limit"""
    all_logs = _sync_list_docs("click_logs")
    filtered = all_logs
    if user_email:
        ue = user_email.strip().lower()
        filtered = [x for x in filtered if ue in x.get("user_email", "").lower()]
    if action_id:
        filtered = [x for x in filtered if action_id in x.get("action_id", "")]
    if days:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        filtered = [x for x in filtered if x.get("timestamp", "") >= cutoff]

    logs = sorted(filtered, key=lambda x: str(x.get("timestamp", "")), reverse=True)
    return logs[:limit]


def db_get_click_logs_df() -> pd.DataFrame:
    """Retrieve click logs as Pandas DataFrame for analytics"""
    logs = db_get_click_logs(limit=5000)
    if not logs:
        return pd.DataFrame(columns=["timestamp", "user_email", "action_id", "ip_address", "user_agent", "referer"])
    df = pd.DataFrame(logs)
    if "id" in df.columns:
        df = df.drop(columns=["id"], errors="ignore")
    return df


# ==============================================================================
# Email Opens (Tracking Pixel) Operations
# ==============================================================================

def db_add_email_open(user_email: str, action_id: str, ip_address: str, user_agent: Optional[str] = None, campaign_id: Optional[str] = None, timestamp: Optional[str] = None) -> str:
    """Insert email open tracking event into Firebase"""
    now = timestamp or datetime.now(timezone.utc).isoformat()
    open_id = f"open_{int(datetime.now(timezone.utc).timestamp()*1000)}_{uuid.uuid4().hex[:6]}"
    open_data = {
        "id": open_id,
        "timestamp": now,
        "user_email": user_email.strip().lower(),
        "action_id": action_id,
        "ip_address": ip_address,
        "user_agent": user_agent or "Unknown",
        "campaign_id": campaign_id or ""
    }

    _sync_set_doc("email_opens", open_id, open_data)
    return open_id


def db_get_email_opens(limit: int = 100) -> List[dict]:
    """Retrieve email opens records"""
    all_opens = _sync_list_docs("email_opens")
    opens = sorted(all_opens, key=lambda x: str(x.get("timestamp", "")), reverse=True)[:limit]
    return opens


def db_get_email_opens_df() -> pd.DataFrame:
    """Retrieve email opens as Pandas DataFrame for analytics"""
    opens = db_get_email_opens(limit=5000)
    if not opens:
        return pd.DataFrame(columns=["timestamp", "user_email", "action_id", "ip_address", "user_agent", "campaign_id"])
    df = pd.DataFrame(opens)
    if "id" in df.columns:
        df = df.drop(columns=["id"], errors="ignore")
    return df


# ==============================================================================
# Flagged Emails Operations
# ==============================================================================

def db_add_flagged_email(email_id: str, sender_email: str, subject: str, flag_category: str, confidence_level: float, user_email: str, threat_level: str, threat_score: float, details: Optional[str] = None) -> str:
    """Insert flagged email threat report into Firebase"""
    now = datetime.now(timezone.utc).isoformat()
    flag_id = f"flag_{uuid.uuid4().hex[:12]}"
    flag_data = {
        "id": flag_id,
        "timestamp": now,
        "email_id": email_id,
        "sender_email": sender_email,
        "subject": subject,
        "flag_category": flag_category,
        "confidence_level": float(confidence_level),
        "user_email": user_email.strip().lower(),
        "threat_level": threat_level,
        "threat_score": float(threat_score),
        "details": details or ""
    }

    _sync_set_doc("flagged_emails", flag_id, flag_data)
    return flag_id


def db_get_flagged_emails(limit: int = 100, category: Optional[str] = None, user_email: Optional[str] = None) -> List[dict]:
    """Retrieve flagged emails with filtering"""
    all_flags = _sync_list_docs("flagged_emails")
    filtered = all_flags
    if category:
        filtered = [x for x in filtered if x.get("flag_category") == category]
    if user_email:
        ue = user_email.strip().lower()
        filtered = [x for x in filtered if ue in x.get("user_email", "").lower()]

    flags = sorted(filtered, key=lambda x: str(x.get("timestamp", "")), reverse=True)[:limit]
    return flags
