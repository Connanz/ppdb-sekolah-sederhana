# Changelog
Semua perubahan penting pada proyek ini akan didokumentasikan dalam file ini.

## [Unreleased]

## [1.0.0] - 2024-05-22
### Added
- Sistem manajemen penerimaan peserta didik baru
- Autentikasi user (siswa) dan admin
- Dashboard admin dan siswa
- Sistem notifikasi email untuk admin dan siswa
- Verifikasi pendaftaran dan pembayaran
- Laporan pendaftaran dalam format Excel
- Filter tanggal bahasa Indonesia

### Features
#### Siswa
- Registrasi dan login akun
- Form pendaftaran dengan upload foto dan dokumen
- Pilihan program studi (Ilmu Komputer, Manajemen Bisnis, Teknik Industri)
- Pilihan agama (Islam, Katolik, Kristen Protestan, Buddha, Hindu, Konghucu)
- Upload dan tracking status pembayaran
- Notifikasi email status pendaftaran
- Dashboard status pendaftaran

#### Admin
- Login dengan verifikasi email
- Dashboard statistik pendaftaran
- Verifikasi pendaftaran siswa
- Verifikasi pembayaran
- Melihat detail data siswa
- Mengubah password
- Laporan dalam format Excel
- Notifikasi email siswa baru
- Catatan verifikasi

### Technical
- Framework: Flask
- Database: SQLite & SQLAlchemy
- Email: SMTP Gmail
- Frontend: TailwindCSS
- DataTables untuk tabel interaktif
- Chart.js untuk visualisasi data
- Export Excel menggunakan XLSX
- Upload file dengan UUID untuk keamanan

### Security
- Password hashing menggunakan Werkzeug
- Role-based access control (Admin/Siswa)
- File upload validation
- Form validation
- Secure filename generation

### Directory Structure
```
PPDB Sekolah/
├── app/
│   ├── routes/
│   ├── static/
│   ├── templates/
│   ├── utils/
│   ├── __init__.py
│   ├── cli.py
│   └── models.py
├── migrations/
├── instance/
├── requirements.txt
├── config.py
└── run.py
```

### Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- Werkzeug
- PyJWT
- Email-validator
- Python-dotenv

### Configuration
- SMTP email setup
- Database configuration
- File upload settings
- Secret key configuration

[1.0.0]: https://github.com/username/ppdb-sekolah/releases/tag/v1.0.0