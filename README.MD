# PPDB Sekolah - Sistem Penerimaan Peserta Didik Baru

Sistem manajemen penerimaan peserta didik baru berbasis web menggunakan Flask dan SQLite.

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

- [Nama Anda]
- [Email]

## Status Proyek

Dalam pengembangan aktif. Silakan buat issue untuk bug report atau feature request.