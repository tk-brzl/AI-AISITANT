"""
教师试卷管理视图
"""
import customtkinter as ctk
from tkinter import messagebox
from services.quiz_service import QuizService
from services.course_service import CourseService


class TeacherQuizView(ctk.CTkFrame):
    """教师试卷管理视图"""

    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.quiz_service = QuizService(db)
        self.course_service = CourseService(db)
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题和创建按钮
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            top_frame,
            text="试卷管理",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        create_btn = ctk.CTkButton(
            top_frame,
            text="生成新试卷",
            width=150,
            command=self.create_quiz_dialog
        )
        create_btn.pack(side="right")

        # 课程选择
        courses = self.course_service.get_teacher_courses(self.user.id)
        if not courses:
            ctk.CTkLabel(
                self,
                text="您还没有创建课程",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        self.courses = courses
        course_frame = ctk.CTkFrame(self)
        course_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            course_frame,
            text="选择课程:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        course_names = [c.name for c in courses]
        self.course_combo = ctk.CTkComboBox(
            course_frame,
            values=course_names,
            width=200,
            command=self.on_course_change
        )
        self.course_combo.pack(side="left", padx=10)
        if course_names:
            self.course_combo.set(course_names[0])

        # 试卷列表
        self.quiz_list_frame = ctk.CTkScrollableFrame(self, label_text="试卷列表")
        self.quiz_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_quizzes()

    def on_course_change(self, choice):
        """课程切换"""
        self.load_quizzes()

    def load_quizzes(self):
        """加载试卷列表"""
        # 清空列表
        for widget in self.quiz_list_frame.winfo_children():
            widget.destroy()

        # 获取当前课程
        current_course = None
        for c in self.courses:
            if c.name == self.course_combo.get():
                current_course = c
                break

        if not current_course:
            return

        # 获取试卷
        quizzes = self.quiz_service.get_course_quizzes(current_course.id)

        if not quizzes:
            ctk.CTkLabel(
                self.quiz_list_frame,
                text="暂无试卷",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        # 显示试卷
        for quiz in quizzes:
            self.create_quiz_card(quiz)

    def create_quiz_card(self, quiz):
        """创建试卷卡片"""
        card = ctk.CTkFrame(self.quiz_list_frame)
        card.pack(fill="x", pady=5, padx=5)

        # 试卷信息
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
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w")

        # 按钮
        btn_frame = ctk.CTkFrame(card)
        btn_frame.pack(side="right", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="查看统计",
            width=100,
            command=lambda q=quiz: self.show_statistics(q)
        ).pack(pady=2)

    def create_quiz_dialog(self):
        """创建试卷对话框"""
        if not hasattr(self, 'courses') or not self.courses:
            messagebox.showwarning("警告", "请先创建课程")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("生成新试卷")
        dialog.geometry("500x450")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # 课程选择
        ctk.CTkLabel(dialog, text="选择课程:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        course_names = [c.name for c in self.courses]
        course_var = ctk.StringVar(value=course_names[0] if course_names else "")
        course_menu = ctk.CTkComboBox(dialog, values=course_names, variable=course_var, width=400)
        course_menu.pack(pady=5)

        # 试卷标题
        ctk.CTkLabel(dialog, text="试卷标题:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        title_entry = ctk.CTkEntry(dialog, width=400, placeholder_text="例如：第一章测验")
        title_entry.pack(pady=5)

        # 知识点
        ctk.CTkLabel(dialog, text="知识点:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        kp_entry = ctk.CTkEntry(dialog, width=400, placeholder_text="例如：Python基础语法")
        kp_entry.pack(pady=5)

        # 题目数量
        ctk.CTkLabel(dialog, text="题目数量:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        count_entry = ctk.CTkEntry(dialog, width=400, placeholder_text="默认10题")
        count_entry.pack(pady=5)

        # 时间限制
        ctk.CTkLabel(dialog, text="时间限制(分钟):", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        time_entry = ctk.CTkEntry(dialog, width=400, placeholder_text="默认30分钟")
        time_entry.pack(pady=5)

        def do_create():
            course_name = course_var.get()
            title = title_entry.get().strip()
            knowledge_point = kp_entry.get().strip()
            count_str = count_entry.get().strip()
            time_str = time_entry.get().strip()

            if not all([course_name, title, knowledge_point]):
                messagebox.showerror("错误", "请填写必填项", parent=dialog)
                return

            # 获取课程ID
            course_id = None
            for c in self.courses:
                if c.name == course_name:
                    course_id = c.id
                    break

            if not course_id:
                messagebox.showerror("错误", "课程不存在", parent=dialog)
                return

            try:
                count = int(count_str) if count_str else 10
                time_limit = int(time_str) if time_str else 30

                self.quiz_service.generate_quiz(
                    self.user.id,
                    course_id,
                    title,
                    knowledge_point,
                    count
                )
                messagebox.showinfo("成功", "试卷生成成功", parent=dialog)
                dialog.destroy()
                self.load_quizzes()
            except Exception as e:
                messagebox.showerror("错误", f"生成失败: {str(e)}", parent=dialog)

        ctk.CTkButton(
            dialog,
            text="生成试卷",
            width=200,
            height=40,
            command=do_create
        ).pack(pady=20)

    def show_statistics(self, quiz):
        """显示试卷统计"""
        try:
            stats = self.quiz_service.get_quiz_statistics(quiz.id, self.user.id)
            
            msg = f"""试卷统计信息

试卷名称: {quiz.title}
知识点: {quiz.knowledge_point}

参与人数: {stats['total_attempts']}
平均分: {stats['average_score']:.1f}
最高分: {stats['max_score']:.1f}
最低分: {stats['min_score']:.1f}
"""
            messagebox.showinfo("统计信息", msg)
        except Exception as e:
            messagebox.showerror("错误", f"获取统计失败: {str(e)}")
