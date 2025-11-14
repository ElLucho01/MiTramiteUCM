from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db
from models.user import User
from notifications import enviar_recordatorio

mail_bp = Blueprint('mail', __name__)

@mail_bp.route("/notificaciones/recordatorio", methods=["POST"])
def notificacion_recordatorio():
    try:
        data = request.get_json(force=True)

        if "email" not in data:
            return jsonify({"error": "Falta el campo 'email' en el JSON"}), 400

        # Datos de ejemplo (en producción serán reales)
        datos_recordatorio = {
            "nombre": data.get("nombre", "Estudiante"),
            "beneficio": data.get("beneficio", "Beca de Alimentación JUNAEB"),
            "fecha_limite": data.get("fecha_limite", "14 de noviembre de 2025"),
            "hora_cierre": data.get("hora_cierre", "17:00 hrs"),
            "horas_restantes": data.get("horas_restantes", 48),
            "cumplidos": data.get("cumplidos", 2),
            "total": data.get("total", 5),
            "porcentaje": data.get("porcentaje", 40),
            "link_web": data.get("link_web", "https://mitramite.ucm.cl/"),
            "link_oficial": data.get("link_oficial", "https://www.junaeb.cl/")
        }

        enviar_recordatorio(data["email"], datos_recordatorio)

        return jsonify({"msg": "Correo HTML enviado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500