from flask_mail import Message
from flask import render_template, current_app

def enviar_correo(destino, asunto, cuerpo):
    # Mantener import aquí evita importaciones circulares
    from app import mail

    with current_app.app_context():
        msg = Message(
            subject=asunto,
            recipients=[destino],
            body=cuerpo
        )
        mail.send(msg)

def enviar_recordatorio(destino, datos):
    # Mantener import aquí evita circular imports
    from app import mail

    # Renderizar la plantilla HTML
    html = render_template(
        "mails/recordatorio.html",     # Ruta correcta (case-sensitive)
        titulo="Recordatorio de Progreso - MiTrámiteUCM",
        nombre=datos["nombre"],
        beneficio=datos["beneficio"],
        fecha_limite=datos["fecha_limite"],
        hora_cierre=datos["hora_cierre"],
        horas_restantes=datos["horas_restantes"],
        cumplidos=datos["cumplidos"],
        total=datos["total"],
        porcentaje=datos["porcentaje"],
        link_web=datos["link_web"],
        link_oficial=datos["link_oficial"]
    )

    # Crear el correo HTML
    msg = Message(
        subject="📢 Recordatorio de tu beneficio",   # Emoji válido, no corrupto
        recipients=[destino],
        html=html
    )

    # Enviar correo
    mail.send(msg)