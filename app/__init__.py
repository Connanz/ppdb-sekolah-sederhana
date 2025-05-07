# Mengimport library yang diperlukan 
from flask import Config, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Inisialisasi Database 
db = SQLAlchemy()