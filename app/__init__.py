# Mengimport library yang diperlukan 
from flask import Config, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
import os
from app.utils.filters import format_indonesian_date

# Inisialisasi Database 
db = SQLAlchemy()

# Inisialisasi Login Manager
login_manager =  LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    # Konfigurasi Aplikasi
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads', 'student_images') # Folder yang menampung foto profil siswa-siswi yang diupload oleh siswa-siswi itu sendiri
    app.config['PAYMENT_UPLOADS'] = os.path.join(app.root_path, 'static', 'uploads', 'payment_proofs') # Folder yang menampung bukti pembayaran dari user/siswa-siswi
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'} # Jenis file yang diizinkan untuk foto profil dan dokumen
    app.config['ALLOWED_PAYMENT_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}  # Jenis file yang diizinkan untuk bukti pembayaran
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # limit yang diberikan hanya 5MB 
    app.config['SECRET_KEY'] = 'mysecret' # Kunci rahasia 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdbsekolah.db' # Nama databse yang digunakan berdasarkan bentuk model yang ada di models.py
    app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi ekstensi
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    # Login Manager mengambil data dari models "User" di database `ppdbsekolah.db`
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Konfigurasi pada models "Form" di models.py dimana filter mengambil data dari setiap user yang login serta 
    @app.context_processor
    def utility_processor():
        def get_latest_form():
            if not current_user.is_authenticated:
                return None
            from app.models import Form
            return Form.query.filter_by(
                user_id=current_user.id
            ).order_by(Form.id.desc()).first()
        return dict(latest_form=get_latest_form())

    # Daftarkan Blueprint
    from .routes import register_blueprints
    register_blueprints(app)

    # Registerasi perintah CLI agar bisa membuat admin di terminal PowerShell
    from .cli import create_admin
    app.cli.add_command(create_admin)

    # Add template filter
    from app.utils.filters import format_indonesian_date
    app.jinja_env.filters['indonesian_date'] = format_indonesian_date

    with app.app_context():
        from app import models # Harus mempunyai file models.py di folder app

    return app