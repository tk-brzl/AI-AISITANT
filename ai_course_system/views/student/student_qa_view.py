"""
学生AI问答视图
"""
import customtkinter as ctk
from tkinter import messagebox
from services.qa_service import QAService
import threading


class StudentQAView(ctk.CTkFrame):
    """学生AI问答视图"""

    def __init__(self, parent, user, db, courses):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.courses = courses
        self.qa_service = QAService(db)
        self.current_course = courses[0] if courses else None
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题和课程选择
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            top_frame,
            text="AI问答助教",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        # 课程选择
        ctk.CTkLabel(
            top_frame,
            text="选择课程:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(40, 10))

        course_names = [c.name for c in self.courses]
        self.course_combo = ctk.CTkComboBox(
            top_frame,
            values=course_names,
            width=200,
            command=self.on_course_change
        )
        self.course_combo.pack(side="left")
        if course_names:
            self.course_combo.set(course_names[0])

        # 对话区域
        self.chat_frame = ctk.CTkScrollableFrame(self, label_text="对话记录")
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 输入区域
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.question_entry = ctk.CTkTextbox(input_frame, height=80)
        self.question_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.ask_btn = ctk.CTkButton(
            input_frame,
            text="提问",
            width=100,
            height=80,
            command=self.ask_question
        )
        self.ask_btn.pack(side="right")

        # 加载历史记录
        self.load_history()

    def on_course_change(self, choice):
        """课程切换"""
        for course in self.courses:
            if course.name == choice:
                self.current_course = course
                self.load_history()
                break

    def load_history(self):
        """加载问答历史"""
        # 清空对话区
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        if not self.current_course:
            return

        # 获取历史记录
        records = self.qa_service.get_user_qa_history(self.user.id, self.current_course.id)

        if not records:
            ctk.CTkLabel(
                self.chat_frame,
                text="暂无问答记录，开始提问吧！",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        # 显示历史记录（最近10条）
        for record in records[:10]:
            self.add_message("问", record.question, is_user=True)
            self.add_message("答", record.answer, is_user=False)

    def add_message(self, label, text, is_user=True):
        """添加消息"""
        msg_frame = ctk.CTkFrame(self.chat_frame)
        msg_frame.pack(fill="x", pady=5, padx=5)

        # 标签
        label_widget = ctk.CTkLabel(
            msg_frame,
            text=label,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=40
        )
        label_widget.pack(side="left", padx=5)

        # 内容
        content_frame = ctk.CTkFrame(msg_frame)
        content_frame.pack(side="left", fill="both", expand=True, padx=5)

        content_label = ctk.CTkLabel(
            content_frame,
            text=text,
            font=ctk.CTkFont(size=12),
            wraplength=700,
            justify="left"
        )
        content_label.pack(anchor="w", padx=10, pady=5)

    def ask_question(self):
        """提问"""
        question = self.question_entry.get("1.0", "end-1c").strip()
        
        if not question:
            messagebox.showwarning("警告", "请输入问题")
            return

        if not self.current_course:
            messagebox.showwarning("警告", "请先选择课程")
            return

        # 禁用按钮
        self.ask_btn.configure(state="disabled", text="思考中...")
        self.question_entry.delete("1.0", "end")

        # 显示问题
        self.add_message("问", question, is_user=True)

        # 在后台线程中调用AI
        def get_answer():
            try:
                result = self.qa_service.ask_question(
                    self.user.id,
                    self.current_course.id,
                    question
                )
                # 在主线程中更新UI
                self.after(0, lambda: self.show_answer(result['answer']))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("错误", f"AI服务错误: {str(e)}"))
            finally:
                self.after(0, lambda: self.ask_btn.configure(state="normal", text="提问"))

        thread = threading.Thread(target=get_answer)
        thread.daemon = True
        thread.start()

    def show_answer(self, answer):
        """显示答案"""
        self.add_message("答", answer, is_user=False)
        # 滚动到底部
        self.chat_frame._parent_canvas.yview_moveto(1.0)
