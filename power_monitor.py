import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# 设置电子邮件参数
sender_email = "sender@example.com"
sender_name = "系统状态预警"
receiver_email = "receiver@example.com"
password = "sender password" 
smtp_server = "smtp server" # 网上查一下邮箱对应的smtp的地址
port = 587  # 通常是587或465


# 发送电子邮件的函数
def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

# 电池电量警告阈值
battery_thresholds = [60, 30, 15, 5]

# 电源和电池状态
power_disconnected = False
battery_level_sent = 100

# 检测电源状态的函数    
# ！文件路径可能不一致
def check_power_status():
    with open("/sys/class/power_supply/ADP0/online", "r") as file:
        status = file.read().strip()
    print(status)
    return status == "0"

# 检测电池电量的函数
def check_battery_level():
    with open("/sys/class/power_supply/BAT0/capacity", "r") as file:
        level = int(file.read().strip())
    print(level)
    return level

#send_email("测试","系统测试")
# 主循环
while True:
    current_power_status = check_power_status()
    battery_level = check_battery_level()

    # 检查电源状态
    if current_power_status:
        if not power_disconnected:
            send_email("电源状态警告", "电源已断开")
            power_disconnected = True
            battery_level_sent = 100  # 重置电池电量警告状态
    else:
        power_disconnected = False

    # 检查电池电量
    if power_disconnected and battery_level < battery_level_sent and battery_level in battery_thresholds:
        send_email("电池电量低", f"电池电量仅剩 {battery_level}%")
        battery_level_sent = battery_level

    time.sleep(60)
