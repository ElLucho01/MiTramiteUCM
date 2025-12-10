from flask import Blueprint, redirect, url_for, session
from models import db
from models.tracking import Beneficios_Estado, Requerimientos_Estado
from models.notification import Notificaciones, UserNotificaciones
from utils import login_required, crear_notificacion_seguimiento
from models.benefit import Beneficios
from flask import session, redirect, url_for


# Añadimos un beneficio a la lista de seguimiento del usuario y redirigimos a la página del beneficio
seguimiento_bp = Blueprint('seguimiento', __name__)

@seguimiento_bp.route('/seguimiento/add/<int:beneficio_id>', methods=['GET'])
@login_required
def agregar_seguimiento(beneficio_id):
    #Obtenemos el id del usuario activo
    user_id = session.get('user_id')
    # Crear una nueva entrada en la tabla Beneficios_Estado
    nuevo_seguimiento = Beneficios_Estado(user_id=user_id, benefit_id=beneficio_id)
    db.session.add(nuevo_seguimiento)
    db.session.commit()
    crear_notificacion_seguimiento(user_id, Beneficios.query.get(beneficio_id))
    return redirect(url_for('home.beneficio_detail', beneficio_id=beneficio_id))

@seguimiento_bp.route('/seguimiento/remove/<int:beneficio_id>', methods=['GET'])
@login_required
def eliminar_seguimiento(beneficio_id):
    #Obtenemos el id del usuario activo
    user_id = session.get('user_id')
    # Buscar la entrada correspondiente en la tabla Beneficios_Estado
    seguimiento = Beneficios_Estado.query.filter_by(user_id=user_id, benefit_id=beneficio_id).first()
    
    if seguimiento:
        db.session.delete(seguimiento)
        db.session.commit()
    
    return redirect(url_for('home.beneficio_detail', beneficio_id=beneficio_id))

@seguimiento_bp.route("/notificaciones/eliminar/<int:notificacion_id>", methods=["DELETE"])
def eliminar_notificacion(notificacion_id):
    user_id = session.get("user_id")

    if not user_id:
        return ({"error": "No autorizado"}), 401

    relacion = UserNotificaciones.query.filter_by(
        user_id=user_id,
        notificacion_id=notificacion_id
    ).first()

    if not relacion:
        return ({"error": "Notificación no encontrada"}), 404

    db.session.delete(relacion)
    db.session.commit()

    # Nuevo: devolver el total de notificaciones restantes
    restantes = UserNotificaciones.query.filter_by(user_id=user_id).count()

    return ({"success": True, "restantes": restantes})


