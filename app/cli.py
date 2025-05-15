import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from .models import db, User, UserRole

# Model CLI untuk membuat admin di terminal PowerShell sesuai dengan ketikan pembuat aplikasi (saya sendiri), tidak dapat berjalan ketika file run.py tengah dijalankan
@click.command('create-admin')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_admin(username, password):
    """Create an admin user."""
    admin = User(
        username=username,
        password=generate_password_hash(password),
        role=UserRole.ADMIN.value
    )
    db.session.add(admin)
    db.session.commit()
    click.echo(f'Created admin user: {username}')