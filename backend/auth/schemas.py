"""
Pydantic schemas for authentication and user accounts
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$")

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
