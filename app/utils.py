from functools import wraps
from flask import session, redirect, url_for, g, Blueprint
from models.tracking import Beneficios_Estado

tracking_loader = Blueprint('tracking_loader', __name__)

#Aseguramos que la sesión esté iniciada
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.index'))  # Página de login
        return f(*args, **kwargs)
    return decorated_function

