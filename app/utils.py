from functools import wraps
from flask import session, redirect, url_for, Blueprint
from models.notification import Notificaciones, UserNotificaciones
from models.benefit_event import Evento_Beneficio
from models.benefit import Beneficios, Requerimientos
from models import db
from datetime import datetime, date, timedelta
import json
import re

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

def crear_notificaciones_eventos(eventos):
    for ev in eventos:
        notif = Notificaciones(
            titulo=f"Falta una semana para: {ev.nombre}",
            mensaje=f"El evento '{ev.nombre}' ocurrirá el {ev.fecha}.",
            tipo="app",
        )
        db.session.add(notif)

    db.session.commit()

    print(f"🔔 Notificaciones creadas: {len(eventos)}")


#Se cargan las fechas importantes desde un archivo JSON
def cargar_eventos_desde_json(ruta_json):
    """Carga datos del JSON a Evento_Beneficio sin usar relaciones."""

    with open(ruta_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    for nombre_evento, fechas in data.items():

        # Prioridad: fecha_inicio -> fecha_publicacion
        if "fecha_inicio" in fechas:
            fecha_str = fechas["fecha_inicio"]

        elif "fecha_publicacion" in fechas:
            fecha_str = fechas["fecha_publicacion"]

        else:
            print(f"Evento ignorado (no tiene fecha válida): {nombre_evento}")
            continue

        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

        evento = Evento_Beneficio(
            nombre=nombre_evento,
            fecha=fecha
        )

        db.session.add(evento)

    db.session.commit()
    print("📌 Eventos cargados correctamente")

#Se cargan los beneficios desde un archivo JSON

def cargar_beneficios_desde_json(ruta_json):
    """Carga beneficios desde un archivo JSON y los inserta en la base de datos."""

    with open(ruta_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    beneficios = data.get("beneficios_detectados", [])

    for beneficio in beneficios:
        nombre = beneficio.get("nombre")
        descripcion = beneficio.get("descripcion")

        # Verificar si existe para evitar duplicados
        existente = Beneficios.query.filter_by(nombre=nombre).first()
        if existente:
            print(f"⚠️ Beneficio ya existe: {nombre}")
            continue

        print(f"➕ Insertando beneficio: {nombre}")

        nuevo_beneficio = Beneficios(
            nombre=nombre,
            descripcion=descripcion,
            fuente=data.get("institucion", "Universidad Católica del Maule"),
            fecha_actualizacion=datetime.utcnow(),
        )

        # Guardar beneficio primero, para que tenga ID
        db.session.add(nuevo_beneficio)
        db.session.flush()
        db.session.commit()

def cargar_requerimientos_desde_json(ruta_json):
    """Carga los requerimientos desde un archivo JSON, sin asociarlos a beneficios."""

    with open(ruta_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        nombre = item.get("nombre")
        documento = item.get("documento")
        pasos = item.get("pasos")

        if not nombre or not documento:
            print(f"Requisito ignorado (faltan campos): {item}")
            continue

        req = Requerimientos(
            nombre=nombre,
            descripcion=documento,
            pasos=pasos
        )

        db.session.add(req)

    db.session.commit()
    print("📌 Requerimientos cargados correctamente")


def eventos_en_una_semana():
    from routes.mail_routes import recordatorio
    """Retorna eventos cuya fecha ocurre exactamente en 7 días."""
    hoy = date.today()
    objetivo = hoy + timedelta(days=7)

    eventos = Evento_Beneficio.query.filter_by(fecha=objetivo).all()
    crear_notificaciones_eventos(eventos)
    recordatorio()
    return eventos