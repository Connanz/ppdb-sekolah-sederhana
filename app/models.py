from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db
from enum import Enum
from datetime import datetime, timezone

class UserRole(Enum):
    STUDENT = 'student'
    ADMIN = 'admin'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.STUDENT.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Forms created/submitted by the user (students)
    submitted_forms = db.relationship('Form',
        backref='submitter',
        foreign_keys='Form.user_id',
        lazy=True
    )

    # Forms verified by the user (admins)
    verified_forms = db.relationship('Form',
        backref='verifier',
        foreign_keys='Form.verified_by',
        lazy=True
    )

    # User's notifications
    notifications = db.relationship('Notification',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def is_admin(self):
        return self.role == UserRole.ADMIN.value

    def is_student(self):
        return self.role == UserRole.STUDENT.value

    def get_dashboard(self):
        """Return the appropriate dashboard URL based on user role"""
        if self.is_admin():
            return 'admin_bp.dashboard'
        return 'form_bp.student_dashboard'

    def get_unread_notifications_count(self):
        """Get count of unread notifications"""
        return Notification.query.filter_by(user_id=self.id, read=False).count()

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_age = db.Column(db.Integer, nullable=False)
    student_email = db.Column(db.String(120), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    document_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    verification_date = db.Column(db.DateTime, nullable=True)
    verification_note = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def create_notification(self, message):
        """Create a notification for the form owner"""
        notification = Notification(
            user_id=self.user_id,
            message=message,
            form_id=self.id
        )
        db.session.add(notification)
        return notification

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)