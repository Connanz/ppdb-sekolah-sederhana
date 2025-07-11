# Kumpulan library untuk mengirim email, lalu karena menggunakan SMTP berbasis kode python maka harus menginstall library smtplib dan email jika tidak bisa menyebabkan error
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import os

class EmailConfig:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'connanztech@gmail.com')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'yljbnsrcwlxggxss')

def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f'PPDB Sekolah <{EmailConfig.SMTP_USERNAME}>'
        msg['To'] = to_email
        msg['Subject'] = subject

        # Convert message to HTML MIMEText
        html_part = MIMEText(message, 'html', 'utf-8')
        msg.attach(html_part)

        # Create SMTP session
        server = smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT)
        server.starttls()
        
        # Login
        server.login(EmailConfig.SMTP_USERNAME, EmailConfig.SMTP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        
        # Close session
        server.quit()
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False