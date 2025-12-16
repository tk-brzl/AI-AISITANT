"""
学生主视图
"""
import customtkinter as ctk
from tkinter import messagebox
from models.database import SessionLocal
from services.course_service import CourseService
from services.qa_service import QAService
from services.quiz_service import QuizService
from .student_course_view import StudentCourseView
from .student_qa_view import StudentQAView
from .student_quiz_view import StudentQuizView
from .student_dashboard_view import StudentDashboardView


class StudentMainView(ctk.CTkFrame):
    """学生主视图"""

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
            ("我的课程", self.show_courses),
            ("AI问答", self.show_qa),
            ("在线测验", self.show_quiz),
            ("学习记录", self.show_dashboard)
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

        # 默认显示课程列表
        self.show_courses()

    def clear_content(self):
        """清空内容区"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_courses(self):
        """显示课程列表"""
        self.clear_content()
        view = StudentCourseView(self.content_frame, self.user, self.db)
        view.pack(fill="both", expand=True)

    def show_qa(self):
        """显示AI问答"""
        self.clear_content()
        
        # 获取学生的课程
        courses = self.course_service.get_student_courses(self.user.id)
        if not courses:
            messagebox.showinfo("提示", "您还没有选课，请先选课")
            self.show_courses()
            return
        
        view = StudentQAView(self.content_frame, self.user, self.db, courses)
        view.pack(fill="both", expand=True)

    def show_quiz(self):
        """显示在线测验"""
        self.clear_content()
        
        # 获取学生的课程
        courses = self.course_service.get_student_courses(self.user.id)
        if not courses:
            messagebox.showinfo("提示", "您还没有选课，请先选课")
            self.show_courses()
            return
        
        view = StudentQuizView(self.content_frame, self.user, self.db, courses)
        view.pack(fill="both", expand=True)

    def show_dashboard(self):
        """显示学习记录"""
        self.clear_content()
        view = StudentDashboardView(self.content_frame, self.user, self.db)
        view.pack(fill="both", expand=True)

    def __del__(self):
        """析构函数"""
        if hasattr(self, 'db'):
            self.db.close()
