from flask import Blueprint, render_template,  redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from app.models import User
from app import db

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index_bp.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth_bp.register'))

        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index_bp.index'))

    return render_template('auth/register.html')
