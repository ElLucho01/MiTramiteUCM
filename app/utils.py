from functools import wraps
from flask import session, redirect, url_for, Blueprint
from models.notification import Notificaciones, UserNotificaciones
from models import db
from datetime import datetime
tracking_loader = Blueprint('tracking_loader', __name__)

#Aseguramos que la sesión esté iniciada
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.index'))  # Página de login
        return f(*args, **kwargs)
    return decorated_function


#Creamos una notificación de seguimiento de beneficio y lo asociamos al usuario
def crear_notificacion_seguimiento(user_id, benefit):
    # Crear notificación
    notif = Notificaciones(
        titulo="Has comenzado a seguir un beneficio",
        mensaje=f"Ahora estás siguiendo el beneficio: {benefit.nombre}",
        tipo="app",
        benefit_id=benefit.id
    )
    db.session.add(notif)
    db.session.flush()  # Para obtener notif.id antes del commit

    # Asociarla al usuario
    user_notif = UserNotificaciones(
        user_id=user_id,
        notificacion_id=notif.id,
        leido=False,
        fecha_recibida=datetime.utcnow()
    )
    db.session.add(user_notif)

    db.session.commit()
    return notif


