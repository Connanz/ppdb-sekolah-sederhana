from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user

student_bp = Blueprint('student_bp', __name__, template_folder='templates')

@student_bp.route('/student_dashboard', methods=['GET'])
def student_dashboard():
    """Render the student dashboard."""
    return render_template('parts/studentdashboard.html', user=current_user)