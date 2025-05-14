from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask import send_from_directory
from app.models import Form, Notification
from app import db
import os
import uuid

form_bp = Blueprint('form_bp', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@form_bp.route('/pendaftaran', methods=['GET', 'POST'])
@login_required
def pendaftaran():
    if request.method == 'POST':
        if 'student_image' not in request.files:
            flash('Harap unggah foto profil', 'error')
            return redirect(request.url)

        file = request.files['student_image']
        
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
            
        if not (file and allowed_file(file.filename)):
            flash('Format file tidak valid. Gunakan JPEG, PNG', 'error')
            return redirect(request.url)

        try:
            # Create uploads directory if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save file with unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)

            # Create form submission
            new_form = Form(
                user_id=current_user.id,
                student_name=request.form.get('student_name'),
                student_age=int(request.form.get('student_age')),
                school_name=request.form.get('school_name'),
                image_path=unique_filename
            )

            db.session.add(new_form)
            db.session.commit()

            flash('Pendaftaran berhasil disubmit!', 'success')
            return redirect(url_for('form_bp.status'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error: {str(e)}")
            flash('Terjadi kesalahan saat mendaftar', 'error')
            return redirect(url_for('form_bp.pendaftaran'))

    return render_template('parts/form.html')

@form_bp.route('/status')
@login_required  # Pastikan user sudah login
def status():
    # Ambil data terakhir yang di-submit oleh user
    latest_submission = Form.query.filter_by(
        user_id=current_user.id
    ).order_by(Form.id.desc()).first()

    if not latest_submission:
        flash('Belum ada data pendaftaran', 'error')
        return redirect(url_for('form_bp.pendaftaran'))

    return render_template(
        'parts/status.html',
        submission=latest_submission,
        # Jika perlu format tanggal:
        # timestamp=latest_submission.timestamp.strftime("%d %B %Y %H:%M")
    )

@form_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@form_bp.route('/student/dashboard')
@login_required
def student_dashboard():
    # Get user's forms
    user_forms = Form.query.filter_by(user_id=current_user.id).order_by(Form.id.desc()).all()
    
    # Get user's notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.timestamp.desc()).limit(5).all()
    
    # Mark notifications as read
    for notification in notifications:
        if not notification.read:
            notification.read = True
    db.session.commit()
    
    return render_template('parts/studentdashboard.html', 
                         user_forms=user_forms,
                         notifications=notifications)