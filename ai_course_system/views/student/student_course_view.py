"""
学生课程视图
"""
import customtkinter as ctk
from tkinter import messagebox
from services.course_service import CourseService


class StudentCourseView(ctk.CTkFrame):
    """学生课程视图"""

    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.course_service = CourseService(db)
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="我的课程",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)

        # 选课按钮
        enroll_btn = ctk.CTkButton(
            self,
            text="选择新课程",
            width=150,
            command=self.show_enroll_dialog
        )
        enroll_btn.pack(pady=10)

        # 课程列表
        self.course_list_frame = ctk.CTkScrollableFrame(self, label_text="已选课程")
        self.course_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_courses()

    def load_courses(self):
        """加载课程列表"""
        # 清空列表
        for widget in self.course_list_frame.winfo_children():
            widget.destroy()

        # 获取学生的课程
        courses = self.course_service.get_student_courses(self.user.id)

        if not courses:
            ctk.CTkLabel(
                self.course_list_frame,
                text="您还没有选课",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        # 显示课程
        for course in courses:
            self.create_course_card(course)

    def create_course_card(self, course):
        """创建课程卡片"""
        card = ctk.CTkFrame(self.course_list_frame)
        card.pack(fill="x", pady=5, padx=5)

        # 课程名称
        name_label = ctk.CTkLabel(
            card,
            text=course.name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack(side="left", padx=20, pady=10)

        # 课程描述
        if course.description:
            desc_label = ctk.CTkLabel(
                card,
                text=course.description[:50] + "..." if len(course.description) > 50 else course.description,
                font=ctk.CTkFont(size=12)
            )
            desc_label.pack(side="left", padx=10)

        # 查看详情按钮
        detail_btn = ctk.CTkButton(
            card,
            text="查看详情",
            width=100,
            command=lambda c=course: self.show_course_detail(c)
        )
        detail_btn.pack(side="right", padx=10, pady=10)

    def show_course_detail(self, course):
        """显示课程详情"""
        # 创建详情对话框
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"课程详情 - {course.name}")
        dialog.geometry("600x400")
        dialog.transient(self.winfo_toplevel())

        # 课程信息
        info_frame = ctk.CTkFrame(dialog)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            info_frame,
            text=course.name,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            info_frame,
            text=f"教师: {course.teacher.real_name}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)

        if course.description:
            desc_text = ctk.CTkTextbox(info_frame, height=100)
            desc_text.pack(fill="x", pady=10)
            desc_text.insert("1.0", course.description)
            desc_text.configure(state="disabled")

        # 课程文档
        ctk.CTkLabel(
            info_frame,
            text="课程资料:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        docs_frame = ctk.CTkScrollableFrame(info_frame, height=150)
        docs_frame.pack(fill="both", expand=True, pady=5)

        documents = self.course_service.get_course_documents(course.id)
        if documents:
            for doc in documents:
                ctk.CTkLabel(
                    docs_frame,
                    text=f"📄 {doc.filename}",
                    font=ctk.CTkFont(size=12)
                ).pack(anchor="w", pady=2)
        else:
            ctk.CTkLabel(
                docs_frame,
                text="暂无课程资料",
                font=ctk.CTkFont(size=12)
            ).pack(pady=10)

    def show_enroll_dialog(self):
        """显示选课对话框"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("选择课程")
        dialog.geometry("600x500")
        dialog.transient(self.winfo_toplevel())

        ctk.CTkLabel(
            dialog,
            text="可选课程",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        # 课程列表
        courses_frame = ctk.CTkScrollableFrame(dialog)
        courses_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 获取所有课程
        all_courses = self.course_service.get_all_courses()
        enrolled_course_ids = [c.id for c in self.course_service.get_student_courses(self.user.id)]

        for course in all_courses:
            if course.id not in enrolled_course_ids:
                self.create_enroll_card(courses_frame, course, dialog)

    def create_enroll_card(self, parent, course, dialog):
        """创建选课卡片"""
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", pady=5, padx=5)

        # 课程信息
        info_frame = ctk.CTkFrame(card)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=course.name,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"教师: {course.teacher.real_name}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")

        # 选课按钮
        def enroll():
            try:
                self.course_service.enroll_student(self.user.id, course.id)
                messagebox.showinfo("成功", f"已成功选课: {course.name}")
                dialog.destroy()
                self.load_courses()
            except Exception as e:
                messagebox.showerror("错误", str(e))

        enroll_btn = ctk.CTkButton(
            card,
            text="选课",
            width=80,
            command=enroll
        )
        enroll_btn.pack(side="right", padx=10, pady=10)
