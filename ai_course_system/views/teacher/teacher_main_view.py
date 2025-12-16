"""
教师主视图
"""
import customtkinter as ctk
from models.database import SessionLocal
from services.course_service import CourseService
from .teacher_course_view import TeacherCourseView
from .teacher_qa_view import TeacherQAView
from .teacher_quiz_view import TeacherQuizView
from .teacher_dashboard_view import TeacherDashboardView


class TeacherMainView(ctk.CTkFrame):
    """教师主视图"""

    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.db = SessionLocal()
        self.course_service = CourseService(self.db)
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 左侧菜单
        menu_frame = ctk.CTkFrame(self, width=200)
        menu_frame.pack(side="left", fill="y", padx=(0, 10))
        menu_frame.pack_propagate(False)

        # 菜单标题
        ctk.CTkLabel(
            menu_frame,
            text="功能菜单",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)

        # 菜单按钮
        menu_items = [
            ("课程管理", self.show_courses),
            ("AI问答", self.show_qa),
            ("试卷管理", self.show_quiz),
            ("数据统计", self.show_dashboard)
        ]

        for text, command in menu_items:
            btn = ctk.CTkButton(
                menu_frame,
                text=text,
                width=180,
                height=40,
                command=command
            )
            btn.pack(pady=5, padx=10)

        # 右侧内容区
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # 默认显示课程管理
        self.show_courses()

    def clear_content(self):
        """清空内容区"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_courses(self):
        """显示课程管理"""
        self.clear_content()
        view = TeacherCourseView(self.content_frame, self.user, self.db)
        view.pack(fill="both", expand=True)

    def show_qa(self):
        """显示AI问答"""
        self.clear_content()
        view = TeacherQAView(self.content_frame, self.user, self.db)
        view.pack(fill="both", expand=True)

    def show_quiz(self):
        """显示试卷管理"""
        self.clear_content()
        view = TeacherQuizView(self.content_frame, self.user, self.db)
        view.pack(fill="both", expand=True)

    def show_dashboard(self):
        """显示数据统计"""
        self.clear_content()
        view = TeacherDashboardView(self.content_frame, self.user, self.db)
        view.pack(fill="both", expand=True)

    def __del__(self):
        """析构函数"""
        if hasattr(self, 'db'):
            self.db.close()
