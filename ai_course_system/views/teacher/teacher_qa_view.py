"""
教师AI问答视图（可查看学生提问）
"""
import customtkinter as ctk
from tkinter import messagebox
from services.qa_service import QAService
from services.course_service import CourseService
import threading


class TeacherQAView(ctk.CTkFrame):
    """教师AI问答视图"""

    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.qa_service = QAService(db)
        self.course_service = CourseService(db)
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="AI问答助教",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # 标签页
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)

        # 我的提问标签
        my_qa_tab = tabview.add("我的提问")
        self.setup_my_qa_tab(my_qa_tab)

        # 学生提问标签
        student_qa_tab = tabview.add("学生提问")
        self.setup_student_qa_tab(student_qa_tab)

    def setup_my_qa_tab(self, parent):
        """设置我的提问标签"""
        # 课程选择
        courses = self.course_service.get_teacher_courses(self.user.id)
        if not courses:
            ctk.CTkLabel(
                parent,
                text="您还没有创建课程",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        top_frame = ctk.CTkFrame(parent)
        top_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            top_frame,
            text="选择课程:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        course_names = [c.name for c in courses]
        course_combo = ctk.CTkComboBox(
            top_frame,
            values=course_names,
            width=200
        )
        course_combo.pack(side="left", padx=10)
        if course_names:
            course_combo.set(course_names[0])

        # 对话区域
        chat_frame = ctk.CTkScrollableFrame(parent)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 输入区域
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(fill="x", padx=10, pady=10)

        question_entry = ctk.CTkTextbox(input_frame, height=80)
        question_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))

        def ask():
            question = question_entry.get("1.0", "end-1c").strip()
            if not question:
                messagebox.showwarning("警告", "请输入问题")
                return

            # 获取当前课程
            current_course = None
            for c in courses:
                if c.name == course_combo.get():
                    current_course = c
                    break

            if not current_course:
                return

            question_entry.delete("1.0", "end")
            
            # 添加问题到对话区
            q_label = ctk.CTkLabel(
                chat_frame,
                text=f"问: {question}",
                font=ctk.CTkFont(size=12),
                wraplength=600,
                justify="left"
            )
            q_label.pack(anchor="w", padx=10, pady=5)

            # 后台获取答案
            def get_answer():
                try:
                    result = self.qa_service.ask_question(self.user.id, current_course.id, question)
                    answer = result['answer']
                    
                    a_label = ctk.CTkLabel(
                        chat_frame,
                        text=f"答: {answer}",
                        font=ctk.CTkFont(size=12),
                        wraplength=600,
                        justify="left"
                    )
                    a_label.pack(anchor="w", padx=10, pady=5)
                except Exception as e:
                    messagebox.showerror("错误", f"AI服务错误: {str(e)}")

            thread = threading.Thread(target=get_answer)
            thread.daemon = True
            thread.start()

        ask_btn = ctk.CTkButton(
            input_frame,
            text="提问",
            width=100,
            height=80,
            command=ask
        )
        ask_btn.pack(side="right")

    def setup_student_qa_tab(self, parent):
        """设置学生提问标签"""
        # 课程选择
        courses = self.course_service.get_teacher_courses(self.user.id)
        if not courses:
            ctk.CTkLabel(
                parent,
                text="您还没有创建课程",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        top_frame = ctk.CTkFrame(parent)
        top_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            top_frame,
            text="选择课程:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        course_names = [c.name for c in courses]
        course_combo = ctk.CTkComboBox(
            top_frame,
            values=course_names,
            width=200
        )
        course_combo.pack(side="left", padx=10)
        if course_names:
            course_combo.set(course_names[0])

        # 刷新按钮
        def refresh():
            load_student_questions(course_combo.get())

        refresh_btn = ctk.CTkButton(
            top_frame,
            text="刷新",
            width=100,
            command=refresh
        )
        refresh_btn.pack(side="left", padx=10)

        # 问题列表
        qa_list_frame = ctk.CTkScrollableFrame(parent)
        qa_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def load_student_questions(course_name):
            # 清空列表
            for widget in qa_list_frame.winfo_children():
                widget.destroy()

            # 获取当前课程
            current_course = None
            for c in courses:
                if c.name == course_name:
                    current_course = c
                    break

            if not current_course:
                return

            # 获取学生提问
            try:
                records = self.qa_service.get_course_qa_history(current_course.id, self.user.id)
                
                if not records:
                    ctk.CTkLabel(
                        qa_list_frame,
                        text="暂无学生提问",
                        font=ctk.CTkFont(size=14)
                    ).pack(pady=20)
                    return

                for record in records[:50]:  # 显示最近50条
                    card = ctk.CTkFrame(qa_list_frame)
                    card.pack(fill="x", pady=5, padx=5)

                    # 学生和时间
                    info_label = ctk.CTkLabel(
                        card,
                        text=f"{record.user.real_name} | {record.created_at.strftime('%Y-%m-%d %H:%M')}",
                        font=ctk.CTkFont(size=10)
                    )
                    info_label.pack(anchor="w", padx=10, pady=(5, 0))

                    # 问题
                    q_label = ctk.CTkLabel(
                        card,
                        text=f"问: {record.question}",
                        font=ctk.CTkFont(size=12),
                        wraplength=700,
                        justify="left"
                    )
                    q_label.pack(anchor="w", padx=10, pady=2)

                    # 答案（可折叠）
                    a_label = ctk.CTkLabel(
                        card,
                        text=f"答: {record.answer[:200]}...",
                        font=ctk.CTkFont(size=11),
                        wraplength=700,
                        justify="left",
                        text_color="gray"
                    )
                    a_label.pack(anchor="w", padx=10, pady=(0, 5))

            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")

        # 初始加载
        if course_names:
            load_student_questions(course_names[0])
