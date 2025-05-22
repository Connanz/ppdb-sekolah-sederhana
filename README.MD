# PPDB Sekolah - Sistem Penerimaan Peserta Didik Baru

Sistem manajemen penerimaan peserta didik baru berbasis web menggunakan Flask dan SQLite.

## Screenshots

### 1. Landing Page & Main Features
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_1.png" alt="Halaman Utama" width="800"/>
  <p><em>1. Halaman Utama PPDB</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_2.png" alt="Dashboard Overview" width="800"/>
  <p><em>2. Dashboard Overview</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_3.png" alt="Statistik Pendaftaran" width="800"/>
  <p><em>3. Statistik Pendaftaran</em></p>
</div>

### 2. Registration Process
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_4.png" alt="Form Pendaftaran" width="800"/>
  <p><em>4. Form Pendaftaran Siswa</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_5.png" alt="Verifikasi Data" width="800"/>
  <p><em>5. Verifikasi Data Pendaftaran</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_6.png" alt="Dashboard Siswa" width="800"/>
  <p><em>6. Dashboard Siswa</em></p>
</div>

### 3. Authentication
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_7.png" alt="Login Page" width="800"/>
  <p><em>7. Halaman Login</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_8.png" alt="Register Page" width="800"/>
  <p><em>8. Halaman Registrasi</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_9.png" alt="Status Verifikasi" width="800"/>
  <p><em>9. Status Verifikasi Akun</em></p>
</div>

### 4. Payment System
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_10.png" alt="Form Pembayaran" width="800"/>
  <p><em>10. Form Pembayaran</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_11.png" alt="Konfirmasi Pembayaran" width="800"/>
  <p><em>11. Konfirmasi Pembayaran</em></p>
</div>

### 5. User Management
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_12.png" alt="Detail User" width="800"/>
  <p><em>12. Detail User</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_13.png" alt="Notifikasi System" width="800"/>
  <p><em>13. Sistem Notifikasi</em></p>
</div>

### 6. Additional Features
<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_14.png" alt="Report Generation" width="800"/>
  <p><em>14. Generasi Laporan</em></p>
</div>

<div align="center">
  <img src="app/static/Documentation%20Images/Screenshots_15.png" alt="Email Notification" width="800"/>
  <p><em>15. Notifikasi Email</em></p>
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

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

## Kontributor

- [Connanz]
- [connanztech@gmail.com]

## Status Proyek

Proyek ini dalam pengembangan aktif oleh pengembang. Silakan laporkan bug atau menambahkan permintaan fitur baru.