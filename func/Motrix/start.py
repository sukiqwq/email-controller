import subprocess
import sys
import time
from xmlrpc import client

subprocess.Popen("./Motrix.exe")
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help') or len(sys.argv) > 4:
    print("Usage: python start.py [url] [file-name] [download-path]")
    sys.exit(1)

# 命令行参数
video_url = sys.argv[1]
output_name = sys.argv[2] if len(sys.argv) >= 3 else ''
download_path = sys.argv[3] if len(sys.argv) == 4 else ''

# RPC 授权秘钥和服务器设置
rpc_token = ''  # 替换成您的 RPC 授权秘钥
server_url = 'http://localhost:16800/rpc'  # 根据需要调整 URL 和端口
s = client.ServerProxy(server_url)

# 尝试执行下载任务，最多重试10次
max_attempts = 10
attempts = 0
while attempts < max_attempts:
    try:
        # 执行下载任务
        s.aria2.addUri('token:' + rpc_token, [video_url], dict(out=output_name))
        # 如果成功，写入成功消息到ref_email.txt并退出循环
        with open("ref_email.txt", "w") as file:
            file.write("download task added successfully")
        print("download task added successfully!")
        break
    except Exception as e:
        print(f"fail in download task adding, try again...（{attempts + 1}/{max_attempts}）")
        attempts += 1
        time.sleep(5)  # 等待1秒后重试

# 如果达到最大尝试次数仍然失败，则写入失败消息到ref_email.txt
if attempts == max_attempts:
    with open("ref_email.txt", "w") as file:
        file.write("download task adding failed, max attempts reached.")
    print("download task adding failed, max attempts reached.")
