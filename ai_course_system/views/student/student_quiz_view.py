"""
学生测验视图
"""
import customtkinter as ctk
from tkinter import messagebox
from services.quiz_service import QuizService
import json


class StudentQuizView(ctk.CTkFrame):
    """学生测验视图"""

    def __init__(self, parent, user, db, courses):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.courses = courses
        self.quiz_service = QuizService(db)
        self.current_course = courses[0] if courses else None
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="在线测验",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # 课程选择
        course_frame = ctk.CTkFrame(self)
        course_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            course_frame,
            text="选择课程:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        course_names = [c.name for c in self.courses]
        self.course_combo = ctk.CTkComboBox(
            course_frame,
            values=course_names,
            width=200,
            command=self.on_course_change
        )
        self.course_combo.pack(side="left", padx=10)
        if course_names:
            self.course_combo.set(course_names[0])

        # 测验列表
        self.quiz_list_frame = ctk.CTkScrollableFrame(self, label_text="可用测验")
        self.quiz_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_quizzes()

    def on_course_change(self, choice):
        """课程切换"""
        for course in self.courses:
            if course.name == choice:
                self.current_course = course
                self.load_quizzes()
                break

    def load_quizzes(self):
        """加载测验列表"""
        # 清空列表
        for widget in self.quiz_list_frame.winfo_children():
            widget.destroy()

        if not self.current_course:
            return

        # 获取课程的测验
        quizzes = self.quiz_service.get_course_quizzes(self.current_course.id)

        if not quizzes:
            ctk.CTkLabel(
                self.quiz_list_frame,
                text="暂无可用测验",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        # 显示测验
        for quiz in quizzes:
            self.create_quiz_card(quiz)

    def create_quiz_card(self, quiz):
        """创建测验卡片"""
        card = ctk.CTkFrame(self.quiz_list_frame)
        card.pack(fill="x", pady=5, padx=5)

        # 测验信息
        info_frame = ctk.CTkFrame(card)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=quiz.title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"知识点: {quiz.knowledge_point}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=2)

        ctk.CTkLabel(
            info_frame,
            text=f"题目数: {len(quiz.questions)}  时限: {quiz.time_limit}分钟",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        # 开始测验按钮
        start_btn = ctk.CTkButton(
            card,
            text="开始测验",
            width=100,
            command=lambda q=quiz: self.start_quiz(q)
        )
        start_btn.pack(side="right", padx=10, pady=10)

    def start_quiz(self, quiz):
        """开始测验"""
        # 创建测验窗口
        quiz_window = ctk.CTkToplevel(self)
        quiz_window.title(f"测验 - {quiz.title}")
        quiz_window.geometry("800x600")
        quiz_window.transient(self.winfo_toplevel())
        quiz_window.grab_set()

        # 创建测验尝试
        try:
            attempt = self.quiz_service.start_quiz(self.user.id, quiz.id)
        except Exception as e:
            messagebox.showerror("错误", str(e))
            quiz_window.destroy()
            return

        # 题目区域
        questions_frame = ctk.CTkScrollableFrame(quiz_window)
        questions_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 存储答案
        answers = {}

        # 显示题目
        for i, question in enumerate(quiz.questions, 1):
            self.create_question_widget(questions_frame, i, question, answers)

        # 提交按钮
        def submit():
            # 检查是否全部作答
            if len(answers) < len(quiz.questions):
                result = messagebox.askyesno("提示", "还有题目未作答，确定提交吗？")
                if not result:
                    return

            # 提交答案
            try:
                for question_id, answer in answers.items():
                    self.quiz_service.submit_answer(attempt.id, question_id, answer)
                
                self.quiz_service.complete_quiz(attempt.id)
                messagebox.showinfo("成功", "测验已提交！")
                quiz_window.destroy()
                self.load_quizzes()
            except Exception as e:
                messagebox.showerror("错误", f"提交失败: {str(e)}")

        submit_btn = ctk.CTkButton(
            quiz_window,
            text="提交测验",
            width=150,
            height=40,
            command=submit
        )
        submit_btn.pack(pady=10)

    def create_question_widget(self, parent, index, question, answers_dict):
        """创建题目控件"""
        q_frame = ctk.CTkFrame(parent)
        q_frame.pack(fill="x", pady=10, padx=5)

        # 题目标题
        title_label = ctk.CTkLabel(
            q_frame,
            text=f"第{index}题 ({question.points}分)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w", padx=10, pady=5)

        # 题目内容
        content_label = ctk.CTkLabel(
            q_frame,
            text=question.question_text,
            font=ctk.CTkFont(size=12),
            wraplength=700,
            justify="left"
        )
        content_label.pack(anchor="w", padx=10, pady=5)

        # 根据题目类型创建答题控件
        if question.question_type in ['choice', 'true_false']:
            # 选择题/判断题
            options = json.loads(question.options)
            answer_var = ctk.StringVar()
            
            for option in options:
                radio = ctk.CTkRadioButton(
                    q_frame,
                    text=option,
                    variable=answer_var,
                    value=option
                )
                radio.pack(anchor="w", padx=30, pady=2)
            
            # 保存答案
            def save_answer(*args):
                answers_dict[question.id] = answer_var.get()
            answer_var.trace('w', save_answer)
        
        else:
            # 简答题
            answer_text = ctk.CTkTextbox(q_frame, height=100)
            answer_text.pack(fill="x", padx=30, pady=5)
            
            def save_answer(*args):
                answers_dict[question.id] = answer_text.get("1.0", "end-1c")
            
            answer_text.bind('<KeyRelease>', save_answer)
