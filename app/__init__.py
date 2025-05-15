# Mengimport library yang diperlukan 
from flask import Config, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
import os

# Inisialisasi Database 
db = SQLAlchemy()

login_manager =  LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    # Konfigurasi Aplikasi
# In your app/__init__.py or where you create the Flask app
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads', 'student_images')
    app.config['PAYMENT_UPLOADS'] = os.path.join(app.config['UPLOAD_FOLDER'], 'payment_proofs')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 2MB limit
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdbsekolah.db'
    app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi ekstensi
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
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

    # Register CLI commands
    from .cli import create_admin
    app.cli.add_command(create_admin)

    with app.app_context():
        from app import models # Harus mempunyai file models.py di folder app

    return app