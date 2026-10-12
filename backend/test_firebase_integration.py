"""
Automated Comprehensive Test Suite for Firebase Integration across Phishy & ThreatLens
Tests:
1. Firebase / Firestore database initialization & seeding
2. User registration with email validation and password hashing
3. Duplicate registration rejection
4. User login & credential authentication
5. Bad password rejection
6. JWT token generation, signature validation, and claims
7. Protected endpoint authorization
8. Click tracking persistence in Firebase
9. Email tracking persistence in Firebase
10. Flagged emails persistence in Firebase
11. FastAPI app startup and health check verification
"""

import os
import sys
import uuid
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app import app
from database import (
    init_db,
    db_get_user_by_email,
    db_get_all_users,
    db_add_click_log,
    db_get_click_logs,
    db_add_email_open,
    db_get_email_opens,
    db_add_flagged_email,
    db_get_flagged_emails,
    verify_password,
    verify_access_token,
    is_live_firebase
)

client = TestClient(app)

def test_database_initialization():
    """Verify that database initializes and seeds default admin users"""
    init_db()
    users = db_get_all_users()
    assert len(users) >= 4, f"Expected at least 4 default users, got {len(users)}"
    
    admin = db_get_user_by_email("admin@phishy.local")
    assert admin is not None
    assert admin["role"] == "admin"
    assert verify_password("admin123", admin["password_hash"])
    assert not admin["password_hash"].startswith("admin123"), "Password must be hashed, never plaintext!"


def test_user_registration_success():
    """Test registering a new unique user"""
    unique_suffix = uuid.uuid4().hex[:6]
    test_email = f"test.registered_{unique_suffix}@phishy.local"
    response = client.post("/auth/register", json={
        "email": test_email,
        "password": "SecurePassword123!",
        "full_name": "Test User",
        "role": "analyst"
    })
    
    assert response.status_code == 200, f"Registration failed: {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert data["user"]["email"] == test_email
    assert data["user"]["role"] == "analyst"
    assert "token" in data
    
    # Verify JWT validity
    token_payload = verify_access_token(data["token"])
    assert token_payload is not None
    assert token_payload["email"] == test_email
    assert token_payload["role"] == "analyst"
    
    # Verify user exists in database with hashed password
    user_in_db = db_get_user_by_email(test_email)
    assert user_in_db is not None
    assert verify_password("SecurePassword123!", user_in_db["password_hash"])
    assert user_in_db["password_hash"] != "SecurePassword123!"


def test_user_registration_duplicate_rejected():
    """Test duplicate registration is rejected with HTTP 400"""
    unique_suffix = uuid.uuid4().hex[:6]
    test_email = f"duplicate.test_{unique_suffix}@phishy.local"
    # First registration
    resp1 = client.post("/auth/register", json={
        "email": test_email,
        "password": "Password123!",
        "full_name": "Original User"
    })
    assert resp1.status_code == 200
    
    # Second registration with same email
    resp2 = client.post("/auth/register", json={
        "email": test_email,
        "password": "DifferentPassword456!",
        "full_name": "Duplicate User"
    })
    assert resp2.status_code == 400
    assert "already exists" in resp2.json()["detail"].lower()


def test_user_login_success():
    """Test user login with valid credentials"""
    response = client.post("/auth/login", json={
        "email": "admin@phishy.local",
        "password": "admin123"
    })
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    assert data["status"] == "success"
    assert data["user"]["email"] == "admin@phishy.local"
    assert "token" in data
    
    payload = verify_access_token(data["token"])
    assert payload is not None
    assert payload["email"] == "admin@phishy.local"


def test_user_login_wrong_password():
    """Test user login rejection when wrong password provided"""
    response = client.post("/auth/login", json={
        "email": "admin@phishy.local",
        "password": "WrongPassword999"
    })
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()


def test_user_login_nonexistent_email():
    """Test user login rejection for unknown email"""
    response = client.post("/auth/login", json={
        "email": "nonexistent.user.12345@phishy.local",
        "password": "SomePassword"
    })
    assert response.status_code == 401


def test_get_all_users():
    """Test retrieving user directory"""
    response = client.get("/auth/users")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "users" in data
    assert len(data["users"]) >= 4
    # Ensure sensitive hashes are not exposed
    for u in data["users"]:
        assert "password_hash" not in u


def test_get_current_user_profile():
    """Test fetching profile with JWT token"""
    login_resp = client.post("/auth/login", json={
        "email": "john.doe@company.com",
        "password": "password123"
    })
    token = login_resp.json()["token"]
    
    # Authorized request with Bearer header
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    user_data = resp.json()["user"]
    assert user_data["email"] == "john.doe@company.com"


def test_click_tracking_persistence():
    """Test tracking click events and persisting in Firebase"""
    test_email = "victim.sim@company.com"
    test_action = "sim_campaign_001"
    
    track_resp = client.get(f"/track/click?user_email={test_email}&action={test_action}", follow_redirects=False)
    assert track_resp.status_code in (302, 307), f"Click tracker should redirect, got {track_resp.status_code}"
    
    logs_resp = client.get(f"/track/logs?user_email={test_email}")
    assert logs_resp.status_code == 200
    logs_data = logs_resp.json()
    assert logs_data["total_records"] >= 1
    matching = [x for x in logs_data["records"] if x["user_email"] == test_email and x["action_id"] == test_action]
    assert len(matching) >= 1


def test_email_opens_tracking():
    """Test email open pixel tracking and persistence"""
    test_email = "open.recipient@company.com"
    test_action = "action_open_001"
    
    pixel_resp = client.get(f"/email-track/pixel/track_pix_123?user_email={test_email}&action={test_action}")
    assert pixel_resp.status_code == 200
    assert pixel_resp.headers["content-type"] == "image/png"
    
    # Verify open records in database
    opens = db_get_email_opens(limit=50)
    matching = [x for x in opens if x["user_email"] == test_email and x["action_id"] == test_action]
    assert len(matching) >= 1


def test_email_flagging_persistence():
    """Test reporting suspicious email and persisting threat record"""
    flag_payload = {
        "email_id": "eml_test_999",
        "sender_email": "attacker@suspicious-domain.xyz",
        "subject": "Urgent Action Required: Verify Bank Account",
        "body": "Please login immediately to secure your account credentials.",
        "flag_category": "phishing",
        "confidence_level": 0.95,
        "user_email": "alert.reporter@company.com",
        "additional_context": "Suspicious spoofed sender"
    }
    
    resp = client.post("/email-flagging/flag", json=flag_payload)
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"
    
    # Verify retrieval
    flags_resp = client.get("/email-flagging/flags?user_email=alert.reporter@company.com")
    assert flags_resp.status_code == 200
    flags_data = flags_resp.json()
    assert flags_data["total_count"] >= 1
    found = [x for x in flags_data["flagged_emails"] if x["email_id"] == "eml_test_999"]
    assert len(found) >= 1


def test_health_check_endpoint():
    """Test health check endpoint reporting Firebase database status"""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "Firebase" in data["database"]["type"]
    assert data["database"]["users_count"] >= 4


if __name__ == "__main__":
    print("Running Firebase integration tests...")
    test_database_initialization()
    print("✓ Database initialization & seeding passed")
    test_user_registration_success()
    print("✓ User registration passed")
    test_user_registration_duplicate_rejected()
    print("✓ Duplicate registration rejection passed")
    test_user_login_success()
    print("✓ User login passed")
    test_user_login_wrong_password()
    print("✓ Wrong password rejection passed")
    test_user_login_nonexistent_email()
    print("✓ Non-existent user rejection passed")
    test_get_all_users()
    print("✓ User directory query passed")
    test_get_current_user_profile()
    print("✓ JWT authentication & profile passed")
    test_click_tracking_persistence()
    print("✓ Click tracking persistence passed")
    test_email_opens_tracking()
    print("✓ Email opens tracking passed")
    test_email_flagging_persistence()
    print("✓ Email flagging persistence passed")
    test_health_check_endpoint()
    print("✓ Health check endpoint passed")
    print("\nALL 12 TESTS PASSED SUCCESSFULLY! 🎉")
