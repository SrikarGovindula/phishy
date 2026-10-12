"""
Authentication database access layer backed by Firebase Firestore
"""

try:
    from database import (
        get_db,
        init_db,
        db_create_user,
        db_get_user_by_email,
        db_get_user_by_id,
        db_update_user_login,
        db_get_all_users,
        db_delete_user
    )
except ImportError:
    from ..database import (
        get_db,
        init_db,
        db_create_user,
        db_get_user_by_email,
        db_get_user_by_id,
        db_update_user_login,
        db_get_all_users,
        db_delete_user
    )

__all__ = [
    "get_db",
    "init_db",
    "db_create_user",
    "db_get_user_by_email",
    "db_get_user_by_id",
    "db_update_user_login",
    "db_get_all_users",
    "db_delete_user"
]
