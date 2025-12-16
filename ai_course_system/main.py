"""
AI线上课程系统 - 主程序入口（修复版）
"""
import sys
import os

# 获取程序运行目录（支持打包后的exe）
if getattr(sys, 'frozen', False):
    # 打包后的exe环境
    application_path = sys._MEIPASS
    sys.path.insert(0, application_path)
else:
    # 开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, application_path)

import customtkinter as ctk
from tkinter import messagebox
from models.database import init_db
from views.login_view import LoginView
from views.main_window import MainWindow
from config import WINDOW_WIDTH, WINDOW_HEIGHT, THEME


class Application(ctk.CTk):
    """主应用程序类"""

    def __init__(self):
        super().__init__()

        # 设置窗口
        self.title("AI线上课程系统")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # 居中显示
        self.center_window()

        # 设置主题
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme(THEME)

        # 初始化数据库
        try:
            init_db()
        except Exception as e:
            messagebox.showerror("错误", f"数据库初始化失败: {str(e)}")
            sys.exit(1)

        # 显示登录界面
        self.show_login()

    def center_window(self):
        """窗口居中"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def show_login(self):
        """显示登录界面"""
        # 清空窗口
        for widget in self.winfo_children():
            widget.destroy()

        # 创建登录视图
        login_view = LoginView(self, self.on_login_success)
        login_view.pack(fill="both", expand=True)

    def on_login_success(self, user):
        """登录成功回调"""
        # 清空窗口
        for widget in self.winfo_children():
            widget.destroy()

        # 创建主窗口
        main_window = MainWindow(self, user, self.on_logout)
        main_window.pack(fill="both", expand=True)

    def on_logout(self):
        """退出登录回调"""
        self.show_login()


def main():
    """主函数"""
    try:
        app = Application()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("错误", f"程序启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
