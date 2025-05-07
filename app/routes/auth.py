from flask import Blueprint, render_template
from flask_login import login_required, current_user

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register')
@login_required 
def register():
    return render_template('auth/register.html', user=current_user)

@auth_bp.route('/login')
@login_required 
def login():
    return render_template('auth/login.html', user=current_user)
