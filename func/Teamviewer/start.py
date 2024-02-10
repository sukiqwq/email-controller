import subprocess
import time

subprocess.Popen("./TeamViewerQS_x64.exe")
time.sleep(20)
import pygetwindow as gw
import pyautogui

# 查找特定名称的窗口
window = gw.getWindowsWithTitle('TeamViewer')[0]

# 确保窗口未最小化且在前台
if window.isMinimized:
    window.restore()
window.activate()
time.sleep(1)
# 获取窗口的位置和大小
left, top, width, height = window.left, window.top, window.width, window.height

# 截取窗口
screenshot = pyautogui.screenshot(region=(left, top, width, height))

# 保存截图
screenshot.save('ref_other.png')

# 生成ref_email.txt
# 正文内容
content = "TeamViewer launched..."

# 创建并写入文件
with open("ref_email.txt", "w") as file:
    file.write(content)

print("ref_email.txt created successfully!")
