import json
import os
import smtplib
import subprocess
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imbox import Imbox

email_addresses = []
action_dic = {}
general_info = {}


def read_config():
    if os.path.exists('general.conf'):
        with open('general.conf', 'r') as file:
            return json.load(file)
    return None


# 写入配置文件
def write_config(data):
    with open('general.conf', 'w') as file:
        json.dump(data, file)


# 删除配置文件
def delete_config():
    if os.path.exists('general.conf'):
        os.remove('general.conf')


def send_email(subject, body, to_email, attachments=None):
    from_email = general_info['email']
    email_password = general_info['password']  # 应该使用更安全的方式存储密码

    # 设置邮件内容
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 附件处理
    if attachments:
        for attachment_path in attachments:
            with open(attachment_path, "rb") as attachment:
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
                msg.attach(p)

    # 发送邮件
    server = smtplib.SMTP(general_info['smtp_host'], 587)
    server.starttls()
    server.login(from_email, email_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


# 核心函数
def core():
    with Imbox(general_info['imap_host'], general_info['email'], general_info['password'], ssl=True) as imbox:

        # 对于列表中的每个邮箱地址，获取并打印所有未读邮件
        for email_address in email_addresses:
            # 获取发件人为列表中邮箱地址的未读邮件
            authored_messages = imbox.messages(unread=True, sent_from=email_address)

            print(f"[debug] Unread messages from {email_address}:")
            for uid, message in authored_messages:
                print(f"[debug] Subject: {message.subject}")  # 邮件主题
                if message.subject == 'emailcontrol':
                    print(message.body['plain'])
                    try:
                        # 读取邮件内容
                        parts = str(message.body['plain'][0]).split('`')
                        # 读取第一行内容
                        keyword = parts[0] if len(parts) > 0 else ""
                        # 读取第二行内容
                        args_list = [part.strip() for part in parts[1:]] if len(parts) > 1 else []
                        # 去掉换行符
                        keyword = keyword.replace("\r\n", "")
                        print("[debug] The first line is：" + keyword)
                        print("[debug] The second line is ：" + str(args_list))
                    except Exception as e:
                        print("[debug] Fail in reading the content:", e)
                        continue
                    # 匹配第一行内容
                    if keyword in action_dic:
                        handle_keyword(keyword, args_list, uid, message, email_address, imbox)
                    else:
                        print("[debug] get keyword:" + keyword)
                        print("[debug] fail in matching keyword:" + keyword + "!")
                        print("[debug] No action will be executed!！")
                else:
                    print("[debug] This is NOT the kind of email that is used for email controllers!")
                    print("[debug] NO action will be executed!")



def handle_keyword(keyword, args_list, uid, message, email_address, imbox):
    print(f"[debug] matched the keyword: {keyword}!")
    temp_address = os.path.join("func", keyword)  # 使用相对路径
    start_script_path = os.path.join(temp_address, "start.py")

    if not os.path.exists(start_script_path):
        print(f"[debug] {start_script_path} NOT exist")
        return

    # 定义run_script函数，整合之前的环境检测和执行逻辑
    def run_script(script_path, args_list=[]):
        """尝试使用系统的Python环境运行脚本。"""
        try:
            # 尝试使用系统的Python运行脚本
            subprocess.run(['python', script_path] + args_list, check=True)
            print("[debug] call system's Python successfully")
        except subprocess.CalledProcessError:
            print("[debug] fail in call system's Python")
        except FileNotFoundError:
            print("[debug] System's Python unavailable")

    # 尝试运行start.py脚本
    print(f"[debug] trying run {start_script_path} script...")
    original_dir = os.getcwd()
    os.chdir(temp_address)  # 更改当前工作目录以确保相对路径的文件能够被正确找到
    run_script("start.py", args_list)

    try:
        # 处理脚本运行后的逻辑
        last_check_time_each_email = time.time()
        while time.time() - last_check_time_each_email < 30:
            if os.path.exists("ref_email.txt"):
                print("[debug] found ref_email.txt!")
                with open("ref_email.txt", "r") as f:
                    email_content = f.read()
                # 检查是否有附件
                attachments = [file for file in os.listdir(".") if file.startswith("ref_other.")]
                send_email("Reply from script", email_content, email_address, attachments)
                # 删除文件
                os.remove("ref_email.txt")
                for attachment in attachments:
                    os.remove(attachment)
                break
            else:
                time.sleep(1)
    finally:
        os.chdir(original_dir)  # 确保无论如何都能返回到原始目录
        imbox.mark_seen(uid)


def run_python_script(script_path):
    with open(script_path, "r") as file:
        script_content = file.read()
    exec(script_content, globals(), locals())


def init():
    global general_info, email_addresses, action_dic
    general_info_json = read_config()
    general_info['imap_host'] = general_info_json['imap_host']
    general_info['smtp_host'] = general_info_json['smtp_host']
    general_info['password'] = general_info_json['password']
    general_info['email'] = general_info_json['email']
    email_addresses.append(general_info['email'])
    # 检查当前目录下是否存在 func 文件夹，若不存在则创建
    func_dir_path = 'func'
    if not os.path.exists(func_dir_path):
        os.makedirs(func_dir_path)
    # 获取 func 文件夹中所有文件夹的名字并存储到列表中
    action_dic = {name: name for name in os.listdir(func_dir_path) if os.path.isdir(os.path.join(func_dir_path, name))}
    print("[debug] The dictionary of the actions:", action_dic)


def run_core():
    while True:
        last_check_time = time.time()
        core()
        print("[debug] waiting new emails...")
        while time.time() - last_check_time < 30:
            time.sleep(1)


if __name__ == '__main__':
    init()
    run_core()
