"""
主窗口 - 根据用户角色显示不同界面
"""
import customtkinter as ctk
from tkinter import messagebox
from auth.session import SessionManager
from .student.student_main_view import StudentMainView
from .teacher.teacher_main_view import TeacherMainView


class MainWindow(ctk.CTkFrame):
    """主窗口"""

    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.on_logout = on_logout
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 顶部栏
        top_frame = ctk.CTkFrame(self, height=60)
        top_frame.pack(fill="x", padx=10, pady=10)
        top_frame.pack_propagate(False)

        # 标题
        role_text = "教师" if self.user.is_teacher() else "学生"
        title_label = ctk.CTkLabel(
            top_frame,
            text=f"AI课程系统 - [{role_text}]",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=20)

        # 用户信息
        user_label = ctk.CTkLabel(
            top_frame,
            text=f"{self.user.real_name}",
            font=ctk.CTkFont(size=14)
        )
        user_label.pack(side="right", padx=10)

        # 退出按钮
        logout_btn = ctk.CTkButton(
            top_frame,
            text="退出登录",
            width=100,
            command=self.logout
        )
        logout_btn.pack(side="right", padx=10)

        # 内容区域
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 根据角色加载不同的视图
        if self.user.is_student():
            self.main_view = StudentMainView(content_frame, self.user)
        else:
            self.main_view = TeacherMainView(content_frame, self.user)
        
        self.main_view.pack(fill="both", expand=True)

    def logout(self):
        """退出登录"""
        result = messagebox.askyesno("确认", "确定要退出登录吗？")
        if result:
            SessionManager.clear_session()
            self.on_logout()
