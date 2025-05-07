from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Form
from app import db

form_bp = Blueprint('form', __name__, template_folder='templates')

@form_bp.route('/pendaftaran', methods=['GET', 'POST'])
@login_required
def pendaftaran():
    if request.method == 'POST':
        # Get form data
        student_name = request.form.get('student_name')
        student_age = request.form.get('student_age')
        school_name = request.form.get('school_name')

        # Validate form data
        if not student_name or not student_age or not school_name:
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('form.pendaftaran'))

        try:
            # Create new form submission
            new_form = Form(
                user_id=current_user.id,
                student_name=student_name,
                student_age=int(student_age),
                school_name=school_name
            )

            # Save to database
            db.session.add(new_form)
            db.session.commit()

            flash('Pendaftaran berhasil disubmit!', 'success')
            return redirect(url_for('form.status'))

        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat mendaftar. Silakan coba lagi.', 'error')
            return redirect(url_for('form.pendaftaran'))

    return render_template('parts/form.html')

@form_bp.route('/status')
@login_required
def status():
    # Get user's form submissions
    submissions = Form.query.filter_by(user_id=current_user.id).all()
    return render_template('form/status.html', submissions=submissions)