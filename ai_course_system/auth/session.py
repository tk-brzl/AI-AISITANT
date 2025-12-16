"""
会话管理
"""


class SessionManager:
    """全局会话管理器"""
    _instance = None
    _current_user = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_current_user(cls, user):
        """设置当前登录用户"""
        cls._current_user = user

    @classmethod
    def get_current_user(cls):
        """获取当前登录用户"""
        return cls._current_user

    @classmethod
    def clear_session(cls):
        """清除会话"""
        cls._current_user = None

    @classmethod
    def is_logged_in(cls):
        """检查是否已登录"""
        return cls._current_user is not None
