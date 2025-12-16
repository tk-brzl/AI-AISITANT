"""
学生数据看板视图
"""
import customtkinter as ctk
from services.qa_service import QAService
from services.quiz_service import QuizService
from services.course_service import CourseService


class StudentDashboardView(ctk.CTkFrame):
    """学生数据看板视图"""

    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.qa_service = QAService(db)
        self.quiz_service = QuizService(db)
        self.course_service = CourseService(db)
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="学习记录",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # 统计卡片区域
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)

        # 获取统计数据
        courses = self.course_service.get_student_courses(self.user.id)
        qa_records = self.qa_service.get_user_qa_history(self.user.id)
        quiz_attempts = self.quiz_service.get_student_attempts(self.user.id)
        completed_quizzes = [a for a in quiz_attempts if a.is_completed]

        # 统计卡片
        self.create_stat_card(stats_frame, "已选课程", str(len(courses)), 0)
        self.create_stat_card(stats_frame, "提问次数", str(len(qa_records)), 1)
        self.create_stat_card(stats_frame, "完成测验", str(len(completed_quizzes)), 2)
        
        if completed_quizzes:
            avg_score = sum(a.score for a in completed_quizzes) / len(completed_quizzes)
            self.create_stat_card(stats_frame, "平均分", f"{avg_score:.1f}", 3)

        # 详细记录区域
        details_frame = ctk.CTkFrame(self)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 标签页
        tabview = ctk.CTkTabview(details_frame)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # 问答历史标签
        qa_tab = tabview.add("问答历史")
        self.show_qa_history(qa_tab, qa_records)

        # 测验记录标签
        quiz_tab = tabview.add("测验记录")
        self.show_quiz_history(quiz_tab, completed_quizzes)

    def create_stat_card(self, parent, title, value, column):
        """创建统计卡片"""
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12)
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(5, 10))

    def show_qa_history(self, parent, records):
        """显示问答历史"""
        if not records:
            ctk.CTkLabel(
                parent,
                text="暂无问答记录",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for record in records[:20]:  # 显示最近20条
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", pady=5, padx=5)

            # 时间和课程
            info_label = ctk.CTkLabel(
                card,
                text=f"{record.created_at.strftime('%Y-%m-%d %H:%M')} | {record.course.name}",
                font=ctk.CTkFont(size=10)
            )
            info_label.pack(anchor="w", padx=10, pady=(5, 0))

            # 问题
            q_label = ctk.CTkLabel(
                card,
                text=f"问: {record.question[:100]}...",
                font=ctk.CTkFont(size=12),
                wraplength=700,
                justify="left"
            )
            q_label.pack(anchor="w", padx=10, pady=2)

    def show_quiz_history(self, parent, attempts):
        """显示测验历史"""
        if not attempts:
            ctk.CTkLabel(
                parent,
                text="暂无测验记录",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for attempt in attempts:
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", pady=5, padx=5)

            # 测验信息
            info_frame = ctk.CTkFrame(card)
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(
                info_frame,
                text=attempt.quiz.title,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                info_frame,
                text=f"完成时间: {attempt.submitted_at.strftime('%Y-%m-%d %H:%M')}",
                font=ctk.CTkFont(size=11)
            ).pack(anchor="w")

            # 分数
            score_label = ctk.CTkLabel(
                card,
                text=f"{attempt.score:.1f}/{attempt.total_points}",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            score_label.pack(side="right", padx=20, pady=10)
