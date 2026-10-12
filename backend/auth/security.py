"""
Security and authentication helper module for Phishy & ThreatLens
"""

try:
    from database import (
        hash_password,
        verify_password,
        create_access_token,
        verify_access_token,
        JWT_SECRET,
        JWT_ALGORITHM,
        JWT_EXPIRATION_MINUTES
    )
except ImportError:
    from ..database import (
        hash_password,
        verify_password,
        create_access_token,
        verify_access_token,
        JWT_SECRET,
        JWT_ALGORITHM,
        JWT_EXPIRATION_MINUTES
    )

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_access_token",
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "JWT_EXPIRATION_MINUTES"
]
