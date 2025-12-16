"""
权限装饰器
"""
from functools import wraps
from .session import SessionManager


def require_role(allowed_roles):
    """
    角色权限装饰器
    
    Args:
        allowed_roles: 允许的角色列表，如 ['teacher'] 或 ['teacher', 'student']
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 获取当前用户
            current_user = SessionManager.get_current_user()

            if not current_user:
                raise PermissionError("用户未登录")

            if current_user.role not in allowed_roles:
                raise PermissionError(f"权限不足，需要角色: {allowed_roles}，当前角色: {current_user.role}")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_login(f):
    """
    登录验证装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SessionManager.is_logged_in():
            raise PermissionError("请先登录")
        return f(*args, **kwargs)
    return decorated_function
