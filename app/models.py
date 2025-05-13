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

    def is_admin(self):
        return self.role == UserRole.ADMIN.value

    def is_student(self):
        return self.role == UserRole.STUDENT.value

    def get_dashboard(self):
        """Return the appropriate dashboard URL based on user role"""
        if self.is_admin():
            return 'admin_bp.dashboard'
        return 'form_bp.student_dashboard'

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_age = db.Column(db.Integer, nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    verification_date = db.Column(db.DateTime, nullable=True)
    verification_note = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)