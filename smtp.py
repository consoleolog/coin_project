import os
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import config

a = {
    'subject': "이것은 메일 제목 입니다",
    'html': """
    <table>
        <thead>
            <tr>
                <th style="width: 18.181818181818183%">일시</th>
                <th style="width: 18.181818181818183%">종목</th>
                <th style="width: 9.090909090909092%">매도/매매</th>
                <th style="width: 27.27272727272727%">가격</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align:center">2023</td>
                <td>btc</td>
                <td style="text-align:center">매매</td>
                <td>1800</td>
            </tr>
        </tbody>
    </table>
    """,
    'filepath': ['./data/btc.csv', './data/eth.csv'],
    'filename': ['btc.csv', 'eth.csv']
}


def send_email(inputs):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = inputs["subject"]
    msg['From'] = config.SMTP_FROM
    msg['To'] = config.SMTP_TO
    html_content = f"""
    {inputs['html']}
    """
    part = MIMEText(html_content, "html")
    msg.attach(part)

    for index, filename in enumerate(inputs['filename']):
        with open(f"{os.getcwd()}/{inputs['filepath'][index]}", "rb") as f:
            file = MIMEBase("application", "octet-stream")
            file.set_payload(f.read())
        encoders.encode_base64(file)
        file.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(file)

    s = smtplib.SMTP('smtp.naver.com', 587)
    s.starttls()  # TLS 보안 처리
    s.login(config.NAVER_ID, config.NAVER_PASSWORD)
    s.sendmail(config.SMTP_FROM, config.SMTP_TO, msg.as_string())
    s.close()


send_email(a)