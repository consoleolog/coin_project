import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv

load_dotenv()


def upload_file(msg, file_content):
    with open(f'./data/{file_content["filename"]}', 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())

    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="post_data.csv"')
    msg.attach(part)


def send_email(content):
    text = content["body"]
    # msg = MIMEText(text)
    msg = MIMEMultipart()
    msg['Subject'] = content["subject"]
    msg['From'] = os.environ["SMTP_FROM"]
    msg['To'] = os.environ["SMTP_TO"]
    msg.attach(MIMEText(text, _charset='utf-8'))

    upload_file(msg, content['file_content'])

    s = smtplib.SMTP('smtp.naver.com', 587)
    s.starttls()  # TLS 보안 처리
    s.login(os.environ["NAVER_ID"], os.environ["NAVER_PASSWORD"])  # 네이버로그인
    s.sendmail(os.environ["SMTP_FROM"], os.environ["SMTP_TO"], msg.as_string())
    s.close()
