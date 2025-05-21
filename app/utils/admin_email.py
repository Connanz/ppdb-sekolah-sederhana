from flask import current_app
from .email_config import send_email

def send_admin_notification(admin_email, student_name):
    try:
        subject = 'Peserta Didik Baru Terdaftar'
        message = f"""
        Kepada Admin,
        
        Dengan ini diberitahukan bahwa:
        
        Nama Siswa: {student_name}
        
        telah berhasil menjadi peserta didik baru di sekolah kita.
        Mohon untuk segera mempersiapkan administrasi yang diperlukan.
        
        Terima kasih,
        Sistem PPDB
        """
        
        return send_email(admin_email, subject, message)
        
    except Exception as e:
        current_app.logger.error(f"Error sending admin notification: {str(e)}")
        return False