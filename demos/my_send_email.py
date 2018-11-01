from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# 输入Email地址和口令:
from email.utils import parseaddr, formataddr

# from_addr = input('From: ')
# password = input('Password: ')  # 我的授权码 mntyryhzalopbchd
# # 输入收件人地址:
# to_addr = input('To: ')
# # 输入SMTP服务器地址: qq.smtp.com
# smtp_server = input('SMTP Server: ')
from_addr = 'wipzhu@126.com'
password = 'zwp949969001'
to_addr = 'wipzhu@qq.com'
smtp_server = 'smtp.126.com'


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# msg = MIMEText('Hello, this is my first letter to you, I am learning Python, so, this letter was send by Python...',
#                'plain', 'utf-8')
# msg = MIMEText('<html><body><h1>Hello</h1><p>send by <a href="http://www.python.org">Python</a>...</p></body></html>',
#                'html', 'utf-8')
msg = MIMEMultipart()
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open('static/blur.png', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='blur.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='blur.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)

# SMTP协议默认端口是25
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
