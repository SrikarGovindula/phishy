"""
Data models and dictionary representations for Firebase Firestore entities
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel

class UserModel(BaseModel):
    id: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    role: str = "user"
    created_at: str
    last_login: Optional[str] = None
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
