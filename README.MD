# PPDB Sekolah - Sistem Penerimaan Peserta Didik Baru

Sistem manajemen penerimaan peserta didik baru berbasis web menggunakan Flask dan SQLite.

## Cuplikan Layar (Screenshots)

### 1. Halaman Depan PPDB Sekolah
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_1.png" alt="Halaman Utama" width="800"/>
  <p><em>1. Halaman Utama PPDB Bagian Atas</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_2.png" alt="Dashboard Overview" width="800"/>
  <p><em>2. Halaman Utama PPDB Bagian Bawah</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_3.png" alt="Statistik Pendaftaran" width="800"/>
  <p><em>3. Persyaratan Pendaftaran PPDB</em></p>
</div>

### 2. Proses Registrasi Pengguna
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_4.png" alt="Form Pendaftaran" width="800"/>
  <p><em>4. Registrasi Pendaftaran User & Admin</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_5.png" alt="Verifikasi Data" width="800"/>
  <p><em>5. Masuk Pendaftaran User & Admin</em></p>
</div>

### 3. Proses Registrasi & Pembayaran Peserta Didik Baru
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_6.png" alt="Dashboard Siswa" width="800"/>
  <p><em>6. Pendaftaran Siswa Baru</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_7.png" alt="Login Page" width="800"/>
  <p><em>7. Status Siswa Setelah Mengirimkan Data Pendaftaran</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_8.png" alt="Register Page" width="800"/>
  <p><em>8. Halaman Informasi Pembayaran</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_9.png" alt="Status Verifikasi" width="800"/>
  <p><em>9. Halaman Upload Bukti Pembayaran</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_10.png" alt="Form Pembayaran" width="800"/>
  <p><em>10. Notifikasi Pembayaran Setelah Mengirimkan Bukti Pembayaran</em></p>
</div>

### 4. Halaman Dashboard Siswa
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_11.png" alt="Konfirmasi Pembayaran" width="800"/>
  <p><em>11. Dashboard Siswa</em></p>
</div>

### 5. Halaman Dashboard Admin
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_12.png" alt="Detail User" width="800"/>
  <p><em>12. Pendaftaran Menunggu Verifikasi</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_13.png" alt="Notifikasi System" width="800"/>
  <p><em>13. Pendaftaran Telah Diverifikasi/Diterima</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_14.png" alt="Report Generation" width="800"/>
  <p><em>14. Pendaftaran Telah Ditolak</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_15.png" alt="Email Notification" width="800"/>
  <p><em>15. Pembayaran Oleh Siswa Yang Menunggu Verifikasi</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_16.png" alt="Email Notification" width="800"/>
  <p><em>16. Pembayaran Oleh Siswa Yang Diterima</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_17.png" alt="Email Notification" width="800"/>
  <p><em>17. Pembayaran Oleh Siswa Yang Ditolak</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_18.png" alt="Email Notification" width="800"/>
  <p><em>18. Detail Siswa Yang Mengirimkan Pendaftaran</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_19.png" alt="Email Notification" width="800"/>
  <p><em>19. Laporan Pendaftaran Siswa Berdasarkan Umur & Sekolah Asal Bagian Atas</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_20.png" alt="Email Notification" width="800"/>
  <p><em>20. Laporan Pendaftaran Siswa Berdasarkan Umur & Sekolah Asal Bagian Bawah</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_21.png" alt="Email Notification" width="800"/>
  <p><em>21. Mengganti Password Admin</em></p>
</div>

### 6. Pemberitahuan Email
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_22.png" alt="Email Notification" width="800"/>
  <p><em>22. Pemberitahuan Pesan Email Kepada Siswa Yang Diverifikasi Oleh Admin</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_23.png" alt="Email Notification" width="800"/>
  <p><em>23. Pemberitahuan Pesan Email Kepada Admin Mengenai Siswa Yang Masuk</em></p>
</div>

## Fitur

### Siswa
- Registrasi dan login akun
- Mengisi formulir pendaftaran
- Upload foto profil dan dokumen pendukung
- Memilih program studi
- Upload bukti pembayaran
- Melihat status pendaftaran
- Menerima notifikasi email

### Admin
- Login dengan verifikasi email
- Dashboard admin
- Verifikasi pendaftaran siswa
- Verifikasi pembayaran
- Melihat detail siswa
- Mengubah password
- Menerima notifikasi email
- Laporan pendaftaran (Excel)

## Teknologi

- Python 3.x
- Flask
- SQLite
- SQLAlchemy
- Flask-Login
- Werkzeug
- TailwindCSS
- DataTables
- Chart.js
- SMTP Email

## Instalasi

1. Clone repository
```bash
git clone https://github.com/username/ppdb-sekolah.git
cd ppdb-sekolah
```

2. Buat virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup database
```bash
flask db upgrade
```

5. Buat admin pertama
```bash
flask create-admin username password admin@email.com
```

6. Jalankan aplikasi
```bash
python run.py
```

## Struktur Folder

```
PPDB Sekolah/
├── app/
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── form.py
│   │   ├── index.py
│   │   └── payment.py
│   ├── static/
│   │   └── uploads/
│   ├── templates/
│   │   ├── auth/
│   │   └── parts/
│   ├── utils/
│   │   ├── admin_email.py
│   │   ├── email.py
│   │   ├── email_config.py
│   │   └── filters.py
│   ├── __init__.py
│   ├── cli.py
│   └── models.py
├── migrations/
├── instance/
├── requirements.txt
├── config.py
└── run.py
```

## Konfigurasi

1. Email SMTP di `app/utils/email_config.py`:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
```

2. Database di `app/__init__.py`:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///ppdbsekolah.db'
```

## Program Studi
- Ilmu Komputer
- Manajemen Bisnis  
- Teknik Industri

## Lisensi

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan
Copyright (c) 2025 [Connanztech]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     
copies of the Software, and to permit persons to whom the Software is         
furnished to do so, subject to the following conditions:                       

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                                

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN     
THE SOFTWARE.

## Kontributor

- [Connanz]
- [connanztech@gmail.com]

## Status Proyek

Proyek ini dalam pengembangan aktif oleh pengembang. Silakan laporkan bug atau menambahkan permintaan fitur baru.