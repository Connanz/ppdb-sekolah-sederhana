from flask import render_template, Blueprint

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')

@index_bp.route('/persyaratan')
def persyaratan():
    return render_template('parts/persyaratan.html')