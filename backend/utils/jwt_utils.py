from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required():
    """
    Decorator to protect routes that require admin access.
    Returns 403 Forbidden if the user's role is not 'admin'.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"message": "Admin access required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
