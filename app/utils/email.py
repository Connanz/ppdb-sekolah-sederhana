# Library untuk mengirim email verifikasi pendaftaran siswa baru ke email peserta didik yang terverifikasi
from flask import current_app
from .email_config import send_email

def send_verification_email(user_email, student_name):
    try:
        subject = 'Pendaftaran Anda Telah Diverifikasi'
        message = f"""
        Yth. {student_name},
        
        Selamat! Anda telah diterima dalam proses pendaftaran siswa baru.
        Pembayaran Anda telah diverifikasi dan pendaftaran Anda telah dikonfirmasi.
        
        Silahkan login ke akun Anda untuk melihat informasi lebih lanjut.
        
        Terima kasih,
        Admin PPDB
        """
        
        return send_email(user_email, subject, message)
        
    except Exception as e:
        current_app.logger.error(f"Error sending verification email: {str(e)}")
        return False