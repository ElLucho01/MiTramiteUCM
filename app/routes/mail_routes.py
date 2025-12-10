from flask import Blueprint, render_template, session, url_for
from flask_mail import Message
from app import mail
from models import db
from models.user import User
from datetime import datetime, timedelta

mail_bp = Blueprint('mail', __name__)

def recuperarContrasena(user):
    """Función auxiliar para enviar el correo de recuperación personalizado"""
    token = user.get_reset_token()
    
    # 1. Generar el enlace (Esto hace que el botón funcione)
    reset_url = url_for('auth.reset_token', token=token, _external=True)
    
    # 2. Calcular fechas para mostrar en el correo
    ahora = datetime.now()
    expira = ahora + timedelta(hours=1) # El token dura 1 hora por defecto en el modelo
    
    # Formatear fechas a texto (ej: 05/12/2025 15:30)
    fecha_solicitud_str = ahora.strftime("%d/%m/%Y %H:%M")
    hora_limite_str = expira.strftime("%H:%M") # Solo la hora para el límite

    # 3. Crear el mensaje
    msg = Message('Recuperación de contraseña - MiTrámiteUCM',
                  sender='noreply@tudominio.com',
                  recipients=[user.correo])
    
    # 4. Renderizar el template pasando LAS VARIABLES EXACTAS que pusiste en tu HTML
    msg.html = render_template('mail/recuperarcontrasena.html', 
                               enlace_recuperacion=reset_url,
                               fecha_solicitud=fecha_solicitud_str,
                               hora_limite=hora_limite_str)
    
    mail.send(msg)

def nuevaCuenta():
    try:
        html = render_template("mail/cuentaCreada.html", nombre = session.get('nombre'), titulo="Cuenta Creada")
        msg = Message(
            subject="Bienvenido a MiTrámiteUCM",
            recipients=[session.get('correo')],
            html = html,
            sender=('MiTramiteUCM', 'luissanmartin0201@gmail.com')
            )
        mail.send(msg)
        return "Correo enviado exitosamente"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"

def recordatorio():
    try:
        usuarios = User.query.all()
        for u in usuarios:
            html = render_template("mail/recordatorio.html", nombre = u.nombre, titulo="Recordatorio de Evento")
            msg = Message(
                subject="Recordatorio de Evento - MiTrámiteUCM",
                recipients=[u.email],
                html = html,
                sender=('MiTramiteUCM', 'luissanmartin0201@gmail.com')
                )
            mail.send(msg)
        return "Correo enviado exitosamente"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"