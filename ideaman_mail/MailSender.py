# coding: utf-8

import smtplib
import time
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ideaman_mail.config import *


def sendEmail(subject,text):
    """
    @subject:邮件标题
    @text：邮件文本
    """
    # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
    subject=Header(subject, 'utf-8').encode()

    # 构造邮件对象MIMEMultipart对象
    # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = '{} <{}>'.format(username,username)
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receiver)
    msg['Date']= time.strftime("%Y-%m-%d", time.localtime())

    # 构造文字内容
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    start_prediction ,end_prediction= 1577894400000,1578412800000

    subject = 'Arxiv 本周推荐论文5篇 : {start_date}-{end_date}'.format(
        start_date=datetime.fromtimestamp(start_prediction / 1000).strftime("%Y.%m.%d"),
        end_date=datetime.fromtimestamp(end_prediction / 1000).strftime("%Y.%m.%d")
    )
    string = """
        1.
    Advanced Intelligent Systems for Surgical Robotics
    Mai Thanh Thai, Phuoc Thien Phan, Shing Wong, Nigel H. Lovell, Thanh Nho Do
    https://arxiv.org/abs/2001.00285v1
    Advanced technologies for sensing, actuation, and intelligent control have enabled multiple surgical devices to simultaneously operate within the human body at low cost and with more efficiency. This paper will overview a historical development of surgery from conventional open to robotic-assisted approaches with discussion on the capabilities of advanced intelligent systems and devices that are currently implemented in existing surgical robotic systems. It will also revisit available autonomous surgical platforms with comments on the essential technologies, existing challenges, and suggestions for the future development of intelligent robotic-assisted surgical systems towards the achievement of fully autonomous operation.
    2.
    Advanced Intelligent Systems for Surgical Robotics
    Mai Thanh Thai, Phuoc Thien Phan, Shing Wong, Nigel H. Lovell, Thanh Nho Do
    https://arxiv.org/abs/2001.00285v1
    Advanced technologies for sensing, actuation, and intelligent control have enabled multiple surgical devices to simultaneously operate within the human body at low cost and with more efficiency. This paper will overview a historical development of surgery from conventional open to robotic-assisted approaches with discussion on the capabilities of advanced intelligent systems and devices that are currently implemented in existing surgical robotic systems. It will also revisit available autonomous surgical platforms with comments on the essential technologies, existing challenges, and suggestions for the future development of intelligent robotic-assisted surgical systems towards the achievement of fully autonomous operation.
    3.
    Advanced Intelligent Systems for Surgical Robotics
    Mai Thanh Thai, Phuoc Thien Phan, Shing Wong, Nigel H. Lovell, Thanh Nho Do
    https://arxiv.org/abs/2001.00285v1
    Advanced technologies for sensing, actuation, and intelligent control have enabled multiple surgical devices to simultaneously operate within the human body at low cost and with more efficiency. This paper will overview a historical development of surgery from conventional open to robotic-assisted approaches with discussion on the capabilities of advanced intelligent systems and devices that are currently implemented in existing surgical robotic systems. It will also revisit available autonomous surgical platforms with comments on the essential technologies, existing challenges, and suggestions for the future development of intelligent robotic-assisted surgical systems towards the achievement of fully autonomous operation.
    """
    sendEmail(subject,string)