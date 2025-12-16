"""
教师数据统计视图
"""
import customtkinter as ctk
from services.course_service import CourseService
from services.qa_service import QAService
from services.quiz_service import QuizService


class TeacherDashboardView(ctk.CTkFrame):
    """教师数据统计视图"""

    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.course_service = CourseService(db)
        self.qa_service = QAService(db)
        self.quiz_service = QuizService(db)
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="数据统计",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # 统计卡片区域
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)

        # 获取统计数据
        courses = self.course_service.get_teacher_courses(self.user.id)
        
        total_students = 0
        total_quizzes = 0
        total_questions = 0
        
        for course in courses:
            total_students += len(course.enrollments)
            quizzes = self.quiz_service.get_course_quizzes(course.id)
            total_quizzes += len(quizzes)
            
            try:
                qa_records = self.qa_service.get_course_qa_history(course.id, self.user.id)
                total_questions += len(qa_records)
            except:
                pass

        # 统计卡片
        self.create_stat_card(stats_frame, "创建课程", str(len(courses)), 0)
        self.create_stat_card(stats_frame, "学生总数", str(total_students), 1)
        self.create_stat_card(stats_frame, "生成试卷", str(total_quizzes), 2)
        self.create_stat_card(stats_frame, "学生提问", str(total_questions), 3)

        # 课程详情
        details_frame = ctk.CTkScrollableFrame(self, label_text="课程详情")
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if not courses:
            ctk.CTkLabel(
                details_frame,
                text="暂无课程数据",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        # 显示每个课程的详细信息
        for course in courses:
            self.create_course_detail_card(details_frame, course)

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

    def create_course_detail_card(self, parent, course):
        """创建课程详情卡片"""
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", pady=5, padx=5)

        # 课程名称
        ctk.CTkLabel(
            card,
            text=course.name,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # 统计信息
        info_frame = ctk.CTkFrame(card)
        info_frame.pack(fill="x", padx=10, pady=5)

        student_count = len(course.enrollments)
        doc_count = len(course.documents)
        quiz_count = len(self.quiz_service.get_course_quizzes(course.id))

        ctk.CTkLabel(
            info_frame,
            text=f"选课学生: {student_count}人  |  课程资料: {doc_count}个  |  测验: {quiz_count}份",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=5, pady=5)

        # 学生列表
        if student_count > 0:
            students_text = "学生: " + ", ".join([e.student.real_name for e in course.enrollments[:10]])
            if student_count > 10:
                students_text += f" 等{student_count}人"
            
            ctk.CTkLabel(
                info_frame,
                text=students_text,
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(anchor="w", padx=5, pady=(0, 10))
