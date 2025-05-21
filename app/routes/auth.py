from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, UserRole
from app import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            if user.is_admin():
                if not email and not user.email:
                    flash('Admin harus mengisi alamat email', 'error')
                    return render_template('auth/login.html', show_admin_email=True)
                
                if email:
                    user.email = email
                    db.session.commit()
            
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for(user.get_dashboard()))
            
        flash('Username atau password salah', 'error')
    
    # Check if admin login is attempted
    show_admin_email = 'admin' in request.args.get('next', '')
    return render_template('auth/login.html', show_admin_email=show_admin_email)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan', 'error')
            return redirect(url_for('auth_bp.register'))

        try:
            # Create new user with student role
            new_user = User(
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                role=UserRole.STUDENT.value
            )

            db.session.add(new_user)
            db.session.commit()

            # Log the user in after registration
            login_user(new_user)
            
            # Redirect to student dashboard
            return redirect(url_for(new_user.get_dashboard()))

        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat mendaftar. Silakan coba lagi.', 'error')
            return redirect(url_for('auth_bp.register'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_bp.index'))

