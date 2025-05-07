from flask import Blueprint, render_template

mod_error = Blueprint('error', __name__)

@mod_error.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404