"""
登录界面
"""
import customtkinter as ctk
from tkinter import messagebox
from models.database import SessionLocal
from models.user import User
from auth.session import SessionManager


class LoginView(ctk.CTkFrame):
    """登录界面"""

    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        self.db = SessionLocal()
        
        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 标题
        title_label = ctk.CTkLabel(
            self,
            text="AI线上课程系统",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=40)

        # 登录表单框
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # 用户名
        ctk.CTkLabel(
            form_frame,
            text="用户名:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(30, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="请输入用户名"
        )
        self.username_entry.pack(pady=5)

        # 密码
        ctk.CTkLabel(
            form_frame,
            text="密码:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(20, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="请输入密码",
            show="*"
        )
        self.password_entry.pack(pady=5)

        # 角色选择
        ctk.CTkLabel(
            form_frame,
            text="角色:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(20, 5))
        
        self.role_var = ctk.StringVar(value="student")
        role_frame = ctk.CTkFrame(form_frame)
        role_frame.pack(pady=5)
        
        ctk.CTkRadioButton(
            role_frame,
            text="学生",
            variable=self.role_var,
            value="student"
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            role_frame,
            text="教师",
            variable=self.role_var,
            value="teacher"
        ).pack(side="left", padx=20)

        # 按钮框
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(pady=30)

        # 登录按钮
        login_btn = ctk.CTkButton(
            button_frame,
            text="登录",
            width=140,
            height=40,
            font=ctk.CTkFont(size=14),
            command=self.login
        )
        login_btn.pack(side="left", padx=10)

        # 注册按钮
        register_btn = ctk.CTkButton(
            button_frame,
            text="注册",
            width=140,
            height=40,
            font=ctk.CTkFont(size=14),
            command=self.register
        )
        register_btn.pack(side="left", padx=10)

        # 绑定回车键
        self.password_entry.bind('<Return>', lambda e: self.login())

    def login(self):
        """登录"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        # 查询用户
        user = self.db.query(User).filter_by(username=username, role=role).first()

        if not user:
            messagebox.showerror("错误", "用户不存在或角色不匹配")
            return

        if not user.check_password(password):
            messagebox.showerror("错误", "密码错误")
            return

        # 登录成功
        SessionManager.set_current_user(user)
        messagebox.showinfo("成功", f"欢迎，{user.real_name}！")
        self.on_login_success(user)

    def register(self):
        """注册"""
        # 创建注册对话框
        dialog = ctk.CTkToplevel(self)
        dialog.title("用户注册")
        dialog.geometry("400x500")
        dialog.transient(self.parent)
        dialog.grab_set()

        # 用户名
        ctk.CTkLabel(dialog, text="用户名:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        username_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="请输入用户名")
        username_entry.pack(pady=5)

        # 密码
        ctk.CTkLabel(dialog, text="密码:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        password_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="请输入密码", show="*")
        password_entry.pack(pady=5)

        # 确认密码
        ctk.CTkLabel(dialog, text="确认密码:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        confirm_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="请再次输入密码", show="*")
        confirm_entry.pack(pady=5)

        # 真实姓名
        ctk.CTkLabel(dialog, text="真实姓名:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        realname_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="请输入真实姓名")
        realname_entry.pack(pady=5)

        # 邮箱
        ctk.CTkLabel(dialog, text="邮箱:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        email_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="请输入邮箱（可选）")
        email_entry.pack(pady=5)

        # 角色
        ctk.CTkLabel(dialog, text="角色:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        role_var = ctk.StringVar(value="student")
        role_frame = ctk.CTkFrame(dialog)
        role_frame.pack(pady=5)
        ctk.CTkRadioButton(role_frame, text="学生", variable=role_var, value="student").pack(side="left", padx=20)
        ctk.CTkRadioButton(role_frame, text="教师", variable=role_var, value="teacher").pack(side="left", padx=20)

        def do_register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            realname = realname_entry.get().strip()
            email = email_entry.get().strip()
            role = role_var.get()

            if not all([username, password, realname]):
                messagebox.showerror("错误", "请填写必填项", parent=dialog)
                return

            if password != confirm:
                messagebox.showerror("错误", "两次密码不一致", parent=dialog)
                return

            # 检查用户名是否已存在
            existing = self.db.query(User).filter_by(username=username).first()
            if existing:
                messagebox.showerror("错误", "用户名已存在", parent=dialog)
                return

            # 创建用户
            user = User(
                username=username,
                real_name=realname,
                role=role,
                email=email
            )
            user.set_password(password)
            self.db.add(user)
            self.db.commit()

            messagebox.showinfo("成功", "注册成功，请登录", parent=dialog)
            dialog.destroy()

        # 注册按钮
        ctk.CTkButton(
            dialog,
            text="注册",
            width=200,
            height=40,
            command=do_register
        ).pack(pady=20)

    def __del__(self):
        """析构函数"""
        if hasattr(self, 'db'):
            self.db.close()
