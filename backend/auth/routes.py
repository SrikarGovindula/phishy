git """
Auth routes re-export
"""

try:
    from routes.auth import router
except ImportError:
    from ..routes.auth import router

__all__ = ["router"]
