"""
教师课程管理视图
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from services.course_service import CourseService
from services.document_service import DocumentService
import os


class TeacherCourseView(ctk.CTkFrame):
    """教师课程管理视图"""

    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.course_service = CourseService(db)
        self.doc_service = DocumentService()
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题和创建按钮
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            top_frame,
            text="课程管理",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        create_btn = ctk.CTkButton(
            top_frame,
            text="创建新课程",
            width=150,
            command=self.create_course_dialog
        )
        create_btn.pack(side="right")

        # 课程列表
        self.course_list_frame = ctk.CTkScrollableFrame(self, label_text="我的课程")
        self.course_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_courses()

    def load_courses(self):
        """加载课程列表"""
        # 清空列表
        for widget in self.course_list_frame.winfo_children():
            widget.destroy()

        # 获取教师的课程
        courses = self.course_service.get_teacher_courses(self.user.id)

        if not courses:
            ctk.CTkLabel(
                self.course_list_frame,
                text="还没有创建课程",
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

        # 课程信息
        info_frame = ctk.CTkFrame(card)
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=course.name,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        if course.description:
            ctk.CTkLabel(
                info_frame,
                text=course.description[:80] + "..." if len(course.description) > 80 else course.description,
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=2)

        # 文档数量
        doc_count = len(course.documents)
        ctk.CTkLabel(
            info_frame,
            text=f"课程资料: {doc_count}个",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w")

        # 按钮区
        btn_frame = ctk.CTkFrame(card)
        btn_frame.pack(side="right", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="上传文档",
            width=100,
            command=lambda c=course: self.upload_document(c)
        ).pack(pady=2)

        ctk.CTkButton(
            btn_frame,
            text="查看详情",
            width=100,
            command=lambda c=course: self.show_course_detail(c)
        ).pack(pady=2)

        ctk.CTkButton(
            btn_frame,
            text="删除课程",
            width=100,
            fg_color="red",
            hover_color="darkred",
            command=lambda c=course: self.delete_course(c)
        ).pack(pady=2)

    def create_course_dialog(self):
        """创建课程对话框"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("创建新课程")
        dialog.geometry("500x400")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # 课程名称
        ctk.CTkLabel(dialog, text="课程名称:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        name_entry = ctk.CTkEntry(dialog, width=400, placeholder_text="请输入课程名称")
        name_entry.pack(pady=5)

        # 课程描述
        ctk.CTkLabel(dialog, text="课程描述:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        desc_text = ctk.CTkTextbox(dialog, width=400, height=150)
        desc_text.pack(pady=5)

        def do_create():
            name = name_entry.get().strip()
            description = desc_text.get("1.0", "end-1c").strip()

            if not name:
                messagebox.showerror("错误", "请输入课程名称", parent=dialog)
                return

            try:
                self.course_service.create_course(self.user.id, name, description)
                messagebox.showinfo("成功", "课程创建成功", parent=dialog)
                dialog.destroy()
                self.load_courses()
            except Exception as e:
                messagebox.showerror("错误", f"创建失败: {str(e)}", parent=dialog)

        ctk.CTkButton(
            dialog,
            text="创建",
            width=200,
            height=40,
            command=do_create
        ).pack(pady=20)

    def upload_document(self, course):
        """上传文档"""
        # 选择文件
        filetypes = [
            ("所有支持的文件", "*.pdf *.docx *.txt"),
            ("PDF文件", "*.pdf"),
            ("Word文档", "*.docx"),
            ("文本文件", "*.txt")
        ]
        filepath = filedialog.askopenfilename(
            title="选择课程文档",
            filetypes=filetypes
        )

        if not filepath:
            return

        try:
            # 读取文件
            with open(filepath, 'rb') as f:
                file_data = f.read()

            # 保存文件
            filename = os.path.basename(filepath)
            saved_path = self.doc_service.save_uploaded_file(file_data, filename, course.id)

            # 上传文档
            self.course_service.upload_document(course.id, self.user.id, saved_path, filename)
            messagebox.showinfo("成功", "文档上传成功")
            self.load_courses()
        except Exception as e:
            messagebox.showerror("错误", f"上传失败: {str(e)}")

    def show_course_detail(self, course):
        """显示课程详情"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"课程详情 - {course.name}")
        dialog.geometry("700x500")
        dialog.transient(self.winfo_toplevel())

        # 课程信息
        info_frame = ctk.CTkFrame(dialog)
        info_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            info_frame,
            text=course.name,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=5)

        if course.description:
            desc_text = ctk.CTkTextbox(info_frame, height=100)
            desc_text.pack(fill="x", pady=10)
            desc_text.insert("1.0", course.description)
            desc_text.configure(state="disabled")

        # 文档列表
        ctk.CTkLabel(
            dialog,
            text="课程资料",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        docs_frame = ctk.CTkScrollableFrame(dialog, height=250)
        docs_frame.pack(fill="both", expand=True, padx=20, pady=10)

        documents = course.documents
        if documents:
            for doc in documents:
                doc_card = ctk.CTkFrame(docs_frame)
                doc_card.pack(fill="x", pady=2, padx=5)

                ctk.CTkLabel(
                    doc_card,
                    text=f"📄 {doc.filename}",
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=10, pady=5)

                ctk.CTkLabel(
                    doc_card,
                    text=f"上传时间: {doc.uploaded_at.strftime('%Y-%m-%d')}",
                    font=ctk.CTkFont(size=10)
                ).pack(side="right", padx=10)
        else:
            ctk.CTkLabel(
                docs_frame,
                text="暂无课程资料",
                font=ctk.CTkFont(size=12)
            ).pack(pady=20)

    def delete_course(self, course):
        """删除课程"""
        result = messagebox.askyesno("确认", f"确定要删除课程 '{course.name}' 吗？\n此操作不可恢复！")
        if result:
            try:
                self.course_service.delete_course(course.id, self.user.id)
                messagebox.showinfo("成功", "课程已删除")
                self.load_courses()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")
