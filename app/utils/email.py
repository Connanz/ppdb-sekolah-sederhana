# Library untuk mengirim email verifikasi pendaftaran siswa baru ke email peserta didik yang terverifikasi
from flask import current_app
from .email_config import send_email
from datetime import datetime
from .filters import format_indonesian_date

def send_verification_email(user_email, student_name):
    try:
        subject = 'Selamat! Pendaftaran Anda Telah Diverifikasi'
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #0066cc; margin-bottom: 20px; text-align: center;">Pemberitahuan Penerimaan Peserta Didik Baru</h2>
        
        <p>Kepada Yth,<br><strong>{student_name}</strong></p>
        
        <p>Dengan senang hati kami informasikan bahwa pendaftaran Anda sebagai calon peserta didik baru telah <strong style="color: #28a745;">BERHASIL DIVERIFIKASI</strong>.</p>
        
        <div style="background-color: #ffffff; padding: 15px; border-left: 4px solid #0066cc; margin: 20px 0;">
            <p style="margin: 0;"><strong>Status:</strong> Terverifikasi</p>
            <p style="margin: 5px 0;"><strong>Tanggal:</strong> {format_indonesian_date(datetime.now())}</p>
        </div>
        
        <p>Langkah selanjutnya:</p>
        <ol style="margin-left: 20px;">
            <li>Silakan melakukan pembayaran sesuai dengan ketentuan</li>
            <li>Upload bukti pembayaran pada sistem PPDB</li>
            <li>Tunggu verifikasi pembayaran dari admin</li>
        </ol>
        
        <p style="margin-top: 20px;">Jika Anda memiliki pertanyaan, silakan hubungi kami di:</p>
        <ul style="list-style: none; padding-left: 0;">
            <li>📧 Email: pendaftaran@sekolah.edu.my.id</li>
            <li>📞 Telepon: +62-821-5558-2475</li>
        </ul>
    </div>
    
    <div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
        <p>Email ini dikirim secara otomatis, mohon tidak membalas email ini.</p>
        <p>© 2025 PPDB Sekolah. All rights reserved.</p>
    </div>
</body>
</html>
"""
        return send_email(user_email, subject, message)
        
    except Exception as e:
        current_app.logger.error(f"Error sending verification email: {str(e)}")
        return False