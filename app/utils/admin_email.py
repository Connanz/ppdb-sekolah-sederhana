# Library untuk mengirim data status peserta didik baru yang sudah diverifikasi untuk ditindaklanjuti
from flask import current_app
from .email_config import send_email
from datetime import datetime

def send_admin_notification(admin_email, student_name):
    try:
        subject = f'[PPDB] Peserta Didik Baru: {student_name}'
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #0066cc; margin-bottom: 20px; text-align: center;">Notifikasi Peserta Didik Baru</h2>
        
        <p>Kepada Admin PPDB,</p>
        
        <div style="background-color: #ffffff; padding: 15px; border-left: 4px solid #0066cc; margin: 20px 0;">
            <p style="margin: 0;"><strong>Informasi Peserta:</strong></p>
            <p style="margin: 5px 0;">Nama: {student_name}</p>
            <p style="margin: 5px 0;">Tanggal Diterima: {datetime.now().strftime('%d %B %Y')}</p>
            <p style="margin: 5px 0;">Status: <span style="color: #28a745;">Terverifikasi</span></p>
        </div>
        
        <p>Tindakan yang diperlukan:</p>
        <ol style="margin-left: 20px;">
            <li>Persiapkan administrasi peserta didik baru</li>
            <li>Update data siswa di sistem akademik</li>
            <li>Siapkan perlengkapan peserta didik baru</li>
        </ol>
        
        <p style="background-color: #e8f4fd; padding: 10px; border-radius: 5px;">
            <strong>Catatan:</strong> Mohon segera tindak lanjuti administrasi untuk peserta didik baru ini.
        </p>
    </div>
    
    <div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
        <p>Email ini dikirim secara otomatis oleh Sistem PPDB Sekolah.</p>
        <p>© 2025 PPDB Sekolah. All rights reserved.</p>
    </div>
</body>
</html>
"""
        return send_email(admin_email, subject, message)
        
    except Exception as e:
        current_app.logger.error(f"Error sending admin notification: {str(e)}")
        return False