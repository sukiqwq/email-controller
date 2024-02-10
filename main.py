import os
import imaplib
import threading
import time

from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox
import core_script
import shutil
import sys
import tempfile



# IMAP 登录验证
def login_imap(imap_host, email, password):
    try:
        mail = imaplib.IMAP4_SSL(imap_host)  # 使用用户提供的IMAP服务器
        mail.login(email, password)
        mail.logout()
        return True
    except imaplib.IMAP4.error:
        return False


# 启动 core_script.py
def start_core_script():
    core_script.init()
    core_script.run_core()


# 创建托盘图标
def create_tray_icon():
    def on_clicked(icon, item):
        icon.stop()
        os._exit(1)

    def logout(icon, item):
        core_script.delete_config()
        messagebox.showinfo('Info', 'Logged out successfully.')

    image = Image.open('src/logo32x32.ico')
    # image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    # draw = ImageDraw.Draw(image)
    # draw.rectangle([0, 0, 64, 64], fill=(0, 0, 0))
    # draw.ellipse([0, 0, 64, 64], fill=(255, 0, 0))

    icon = pystray.Icon("test_icon", image, "Email Controller",
                        menu=pystray.Menu(item('Logout', logout), item('Exit', on_clicked)))
    icon.run()


# 显示登录窗口
def show_login_window():
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="IMAP Host:").grid(row=0)
    tk.Label(root, text="SMTP Host:").grid(row=1)  # 添加 SMTP Host 输入
    tk.Label(root, text="Email:").grid(row=2)
    tk.Label(root, text="Password:").grid(row=3)

    imap_host_entry = tk.Entry(root)
    smtp_host_entry = tk.Entry(root)  # SMTP Host 输入框
    email_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")

    imap_host_entry.grid(row=0, column=1)
    smtp_host_entry.grid(row=1, column=1)  # 布局 SMTP Host 输入框
    email_entry.grid(row=2, column=1)
    password_entry.grid(row=3, column=1)

    def try_login():
        imap_host = imap_host_entry.get()
        smtp_host = smtp_host_entry.get()  # 获取 SMTP Host
        email = email_entry.get()
        password = password_entry.get()

        if login_imap(imap_host, email, password):  # 假设您的验证函数同时适用于IMAP和SMTP
            # 保存登录信息到配置文件
            config_data = {
                'imap_host': imap_host,
                'smtp_host': smtp_host,  # 保存 SMTP Host
                'email': email,
                'password': password
            }
            core_script.write_config(config_data)
            messagebox.showinfo('Info', 'Logged in successfully.')
            root.destroy()
            create_tray_icon()
            start_core_script()

        else:
            messagebox.showerror('Error', 'Login failed.')

    tk.Button(root, text="Login", command=try_login).grid(row=4, column=1)
    root.mainloop()


def start_tray_icon_in_thread():
    # 在线程中启动托盘图标
    tray_thread = threading.Thread(target=create_tray_icon)
    tray_thread.daemon = True  # 设置为守护线程，确保主程序退出时托盘图标线程也会退出
    tray_thread.start()


# 主函数
def main():
    config = core_script.read_config()
    if config and login_imap(config['imap_host'], config['email'], config['password']):
        print("login success")
    else:
        show_login_window()
    start_tray_icon_in_thread()
    start_core_script()


if __name__ == '__main__':
    main()

