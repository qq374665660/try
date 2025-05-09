# reminder.py
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
import sqlite3

def check_deadlines():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM projects WHERE progress < 100 AND deadline < DATE('now')")
    overdue_projects = cursor.fetchall()
    
    if overdue_projects:
        # 发送邮件
        msg = MIMEText(f"逾期课题：{', '.join([p[0] for p in overdue_projects])}")
        msg['Subject'] = '课题逾期警告'
        server = smtplib.SMTP('smtp.example.com', 587)
        server.login('your_email@example.com', 'password')
        server.sendmail('sender@example.com', 'receiver@example.com', msg.as_string())
        server.quit()

# 启动定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(check_deadlines, 'interval', hours=24)
scheduler.start()