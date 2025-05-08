from .index import index_bp
from .auth import auth_bp
from .error import mod_error
from .form import form_bp
from .admin import admin_bp

# Tempat untuk Registerasi semua route dari blueprint yang ada di dalam folder routes
def register_blueprints(app):
    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(mod_error, url_prefix='/error')
    app.register_blueprint(form_bp, url_prefix='/form')
    app.register_blueprint(admin_bp, url_prefix='/admin')