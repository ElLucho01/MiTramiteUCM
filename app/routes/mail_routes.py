from flask import Blueprint, render_template, session
from flask_mail import Message
from app import mail

mail_bp = Blueprint('mail', __name__)

def nuevaCuenta():
    try:
        html = render_template("mail/cuentaCreada.html", nombre = session.get('nombre'), titulo="Cuenta Creada")
        msg = Message(
            subject="Prueba de correo HTML",
            recipients=[session.get('correo')],
            html = html,
            sender=('MiTramiteUCM', 'luissanmartin0201@gmail.com')
            )
        mail.send(msg)
        return "Correo enviado exitosamente"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"
    
#@mail_bp.route("/test2/")
#def nuevoSeguimiento():
#    try:
#        html = render_template("mail/nuevoSeguimiento.html", nombre = session.get('user_name'), titulo="Nuevo Seguimiento")
#        msg = Message(
#            subject="Prueba de correo HTML",
#            recipients=["

