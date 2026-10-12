import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import re
from fastapi import APIRouter, HTTPException, Depends, Header, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse

from database import (
    db_create_user,
    db_get_user_by_email,
    db_get_user_by_id,
    db_update_user_login,
    db_update_user_password,
    db_get_all_users,
    db_delete_user,
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)

router = APIRouter()
logger = logging.getLogger(__name__)
security_bearer = HTTPBearer(auto_error=False)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$")

# ==============================================================================
# Request & Response Schemas
# ==============================================================================

class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")
    full_name: Optional[str] = Field(None, description="Full name")
    role: Optional[str] = Field("user", description="User role (user, admin, analyst)")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format")
        return clean

class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="Password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format")
        return clean

class GoogleAuthRequest(BaseModel):
    email: str = Field(..., description="Google account email")
    full_name: Optional[str] = Field(None, description="User full name")
    google_id: Optional[str] = Field(None, description="Google UID / subject")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format")
        return clean

class ResetPasswordRequest(BaseModel):
    email: str = Field(..., description="User email address")
    new_password: Optional[str] = Field(None, min_length=6, description="New password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format")
        return clean

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    role: str = "user"
    created_at: str
    last_login: Optional[str] = None

class AuthResponse(BaseModel):
    status: str
    message: str
    token: str
    token_type: str = "Bearer"
    user: UserResponse


# ==============================================================================
# Authentication Dependencies
# ==============================================================================

def get_current_user(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    token_query: Optional[str] = Query(None, alias="token")
) -> Optional[dict]:
    """Extract and validate JWT access token to get authenticated user"""
    raw_token = None
    if auth_header and auth_header.credentials:
        raw_token = auth_header.credentials
    elif token_query:
        raw_token = token_query

    if not raw_token:
        return None

    payload = verify_access_token(raw_token)
    if not payload:
        return None

    user_id = payload.get("sub")
    email = payload.get("email")

    user = None
    if user_id:
        user = db_get_user_by_id(user_id)
    if not user and email:
        user = db_get_user_by_email(email)

    return user


def require_authenticated_user(current_user: Optional[dict] = Depends(get_current_user)) -> dict:
    """Dependency that enforces active authentication"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided or are invalid",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return current_user


# ==============================================================================
# Endpoints
# ==============================================================================

@router.post("/register", response_model=AuthResponse)
def register_user(request: UserRegisterRequest):
    """
    Register a new user in Firebase / Firestore database
    """
    email_clean = str(request.email).lower().strip()
    
    # Check if user already exists
    existing = db_get_user_by_email(email_clean)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    pw_hash = hash_password(request.password)
    user_role = request.role or "user"
    full_name = request.full_name or email_clean.split('@')[0].capitalize()
    
    user_doc = db_create_user(
        email=email_clean,
        password_hash=pw_hash,
        full_name=full_name,
        role=user_role
    )
    
    # Generate signed JWT token
    token = create_access_token({
        "sub": str(user_doc["id"]),
        "email": user_doc["email"],
        "role": user_doc["role"]
    })
    
    user_data = UserResponse(
        id=str(user_doc["id"]),
        email=user_doc["email"],
        full_name=user_doc.get("full_name"),
        role=user_doc.get("role", "user"),
        created_at=user_doc.get("created_at", ""),
        last_login=user_doc.get("last_login")
    )
    
    logger.info(f"Registered new user in Firebase DB: {email_clean} (ID: {user_doc['id']})")
    
    return AuthResponse(
        status="success",
        message="Registration successful",
        token=token,
        token_type="Bearer",
        user=user_data
    )


@router.post("/login", response_model=AuthResponse)
def login_user(request: UserLoginRequest):
    """
    Authenticate user against Firebase / Firestore database
    """
    email_clean = str(request.email).lower().strip()
    user_doc = db_get_user_by_email(email_clean)
    
    if not user_doc or not verify_password(request.password, user_doc.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    now = datetime.now(timezone.utc).isoformat()
    db_update_user_login(user_doc["id"], now)
    
    token = create_access_token({
        "sub": str(user_doc["id"]),
        "email": user_doc["email"],
        "role": user_doc.get("role", "user")
    })
    
    user_data = UserResponse(
        id=str(user_doc["id"]),
        email=user_doc["email"],
        full_name=user_doc.get("full_name"),
        role=user_doc.get("role", "user"),
        created_at=user_doc.get("created_at", now),
        last_login=now
    )
    
    logger.info(f"User logged in from Firebase DB: {email_clean}")
    
    return AuthResponse(
        status="success",
        message="Login successful",
        token=token,
        token_type="Bearer",
        user=user_data
    )


@router.post("/google", response_model=AuthResponse)
def google_auth(request: GoogleAuthRequest):
    """
    Authenticate or auto-provision a user signing in via Google Identity / Firebase Google Auth
    """
    email_clean = str(request.email).lower().strip()
    user_doc = db_get_user_by_email(email_clean)
    now = datetime.now(timezone.utc).isoformat()
    
    if not user_doc:
        # Auto-provision user with Google identity in Firebase database
        dummy_pwd = hash_password(f"google_{request.google_id or email_clean}_{now}")
        full_name = request.full_name or email_clean.split("@")[0].replace(".", " ").title()
        user_doc = db_create_user(
            email=email_clean,
            password_hash=dummy_pwd,
            full_name=full_name,
            role="user"
        )
        logger.info(f"Auto-provisioned new Google user in Firebase DB: {email_clean}")
    else:
        db_update_user_login(user_doc["id"], now)
        logger.info(f"Existing Google user logged in: {email_clean}")

    token = create_access_token({
        "sub": str(user_doc["id"]),
        "email": user_doc["email"],
        "role": user_doc.get("role", "user")
    })
    
    user_data = UserResponse(
        id=str(user_doc["id"]),
        email=user_doc["email"],
        full_name=user_doc.get("full_name"),
        role=user_doc.get("role", "user"),
        created_at=user_doc.get("created_at", now),
        last_login=now
    )
    
    return AuthResponse(
        status="success",
        message="Google sign-in successful",
        token=token,
        token_type="Bearer",
        user=user_data
    )


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    """
    Verify user exists and update password or issue reset confirmation
    """
    email_clean = str(request.email).lower().strip()
    user_doc = db_get_user_by_email(email_clean)
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No account found matching {email_clean}"
        )
        
    if request.new_password:
        if len(request.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long"
            )
        new_hash = hash_password(request.new_password)
        db_update_user_password(user_doc["id"], new_hash)
        logger.info(f"Password reset successfully updated in Firebase DB for {email_clean}")
        return JSONResponse(content={
            "status": "success",
            "message": f"Password for {email_clean} has been successfully updated. You may now sign in."
        })
    else:
        # Password reset initiation check
        return JSONResponse(content={
            "status": "success",
            "message": f"Account verified for {email_clean}. You can now provide your new password.",
            "email": email_clean
        })


@router.get("/users")
def get_all_users():
    """
    Get list of all users stored in Firebase database
    """
    users = db_get_all_users()
    # Strip sensitive password_hash before returning
    safe_users = []
    for u in users:
        safe_users.append({
            "id": str(u.get("id")),
            "email": u.get("email"),
            "full_name": u.get("full_name"),
            "role": u.get("role", "user"),
            "created_at": u.get("created_at"),
            "last_login": u.get("last_login")
        })

    return JSONResponse(content={
        "status": "success",
        "total_users": len(safe_users),
        "users": safe_users
    })


@router.get("/me")
def get_current_user_profile(
    user_email: Optional[str] = Query(None),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get profile for currently authenticated user or requested user email
    """
    if current_user:
        safe_user = {
            "id": str(current_user.get("id")),
            "email": current_user.get("email"),
            "full_name": current_user.get("full_name"),
            "role": current_user.get("role", "user"),
            "created_at": current_user.get("created_at"),
            "last_login": current_user.get("last_login")
        }
        return JSONResponse(content={
            "status": "success",
            "user": safe_user
        })

    # Fallback to query email if specified, or default admin
    target_email = user_email or "admin@phishy.local"
    user_doc = db_get_user_by_email(target_email)
    
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
        
    safe_user = {
        "id": str(user_doc.get("id")),
        "email": user_doc.get("email"),
        "full_name": user_doc.get("full_name"),
        "role": user_doc.get("role", "user"),
        "created_at": user_doc.get("created_at"),
        "last_login": user_doc.get("last_login")
    }

    return JSONResponse(content={
        "status": "success",
        "user": safe_user
    })


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    """
    Delete a user from Firebase database
    """
    success = db_delete_user(user_id)
    if not success:
        # Check if user exists
        user = db_get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
            
    return JSONResponse(content={
        "status": "success",
        "message": f"User {user_id} deleted successfully"
    })
