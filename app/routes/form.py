from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Form
from app import db
import os
import uuid

form_bp = Blueprint('form', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@form_bp.route('/pendaftaran', methods=['GET', 'POST'])
@login_required
def pendaftaran():
    if request.method == 'POST':
        # Handle file upload first
        if 'student_image' not in request.files:
            flash('Harap unggah foto profil', 'error')
            return redirect(request.url)

        file = request.files['student_image']
        
        # Validate file
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
            
        if not (file and allowed_file(file.filename)):
            flash('Format file tidak valid. Gunakan JPEG, PNG', 'error')
            return redirect(request.url)

        # Process form data
        student_name = request.form.get('student_name')
        student_age = request.form.get('student_age')
        school_name = request.form.get('school_name')

        # Validate all fields
        if not all([student_name, student_age, school_name]):
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('form.pendaftaran'))

        try:
            # Save the file
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, unique_filename))

            # Create new form submission
            new_form = Form(
                user_id=current_user.id,
                student_name=student_name,
                student_age=int(student_age),
                school_name=school_name,
                image_path=unique_filename  # Add image path
            )

            db.session.add(new_form)
            db.session.commit()

            flash('Pendaftaran berhasil disubmit!', 'success')
            return redirect(url_for('form.status'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error during registration: {str(e)}")
            flash('Terjadi kesalahan saat mendaftar. Silakan coba lagi.', 'error')
            return redirect(url_for('form.pendaftaran'))

    return render_template('parts/form.html')