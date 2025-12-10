from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mail import Message # Nueva importación para enviar correos
from models import db
from models.user import User
from utils import login_required
from .mail_routes import nuevaCuenta, recuperarContrasena
# Asegúrate de importar datetime y timedelta al inicio del archivo
from datetime import datetime, timedelta

# IMPORTANTE: Ajusta esta importación según donde hayas inicializado 'mail' en tu proyecto.
# Podría ser 'from app import mail' o 'from . import mail' si estás en un paquete.
from app import mail 

auth_bp = Blueprint('auth', __name__)

#Al abrir la pagina principal al no tener sesión iniciada
@auth_bp.route('/register')
def printScreen():
    return render_template('login.html')

 #En caso de pulsar el boton de registrar
@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    error = None
    #Se registran los datos del formulario de registro
    nombre = request.form.get('nombreReg')
    correo = request.form.get('correoReg')
    correoB = request.form.get('correoRegB')
    contrasena = request.form.get('contrasenaReg')
    contrasenaB = request.form.get('contrasenaRegB')

    #Se comprueba que el correo no esté ya registrado
    usuario = User.query.filter_by(correo=correo).first()
    #Se comprueban los posibles errores de entrada
    if usuario:
        error = 'El correo ya está registrado. Por favor, inicia sesión.'
        flash(error, 'error')
    elif correo != correoB:
        error = 'Los correos no coinciden. Inténtalo de nuevo.'
        flash(error, 'error')
    elif contrasena != contrasenaB:
        error = 'Las contraseñas no coinciden. Inténtalo de nuevo.'
        flash(error, 'error')
    if(error):
        return redirect(url_for('auth.printScreen'))
    usuario = User(nombre=nombre, correo=correo)
    usuario.set_password(contrasena)
    #Se añade el usuario a la base de datos
    db.session.add(usuario)
    db.session.commit()
    #Se registra la información en la sesión
    log_user(usuario)
    nuevaCuenta()
    return redirect(url_for('home.home'))

#En caso de iniciar sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    #Se leen los datos del formulario de login
    correo = request.form.get('correoLog')
    contrasena = request.form.get('contrasenaLog')
    usuario = User.query.filter_by(correo=correo).first()
    if usuario and usuario.check_password(contrasena):
        #Login exitoso, redirigir a la página de inicio
        log_user(usuario)
        return redirect(url_for('home.home'))
    else:
        #Login fallido, redirigir a la página principal (agregar mensaje de error)
        flash('Correo o contraseña incorrectos. Inténtalo de nuevo.', 'error')
        return redirect(url_for('auth.printScreen'))
    
#Cerrar Sesión
@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home.home'))

@auth_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Ruta para solicitar el correo de recuperación"""
    # Si ya está logueado, no necesita recuperar
    if 'user_id' in session:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        email = request.form.get('email') # Asegúrate que tu input HTML tenga name="email"
        user = User.query.filter_by(correo=email).first()
        
        if user:
            recuperarContrasena(user)
            flash('Se ha enviado un correo con instrucciones para restablecer tu contraseña.', 'info')
            return redirect(url_for('auth.printScreen'))
        else:
            flash('No se encontró cuenta con ese correo.', 'error')

    # Renderiza el formulario donde piden el correo
    return render_template('reset_request.html') 

@auth_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Ruta para validar el token y cambiar la contraseña"""
    if 'user_id' in session:
        return redirect(url_for('home.home'))

    # Verificar token usando el método estático del modelo User
    user = User.verify_reset_token(token)
    
    if user is None:
        flash('El enlace es inválido o ha expirado.', 'error')
        return redirect(url_for('auth.reset_request'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        password_confirm = request.form.get('confirm_password')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden.', 'error')
            # Renderiza de nuevo el formulario de cambio si fallan
            return render_template('reset_token.html') 

        # Establecer nueva contraseña y guardar
        user.set_password(password)
        db.session.commit()
        
        flash('Tu contraseña ha sido actualizada. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.printScreen'))

    # Renderiza el formulario para poner la nueva contraseña
    return render_template('reset_token.html')

#Se cargan los datos del usuario en la sesión
def log_user(usuario):
    session['user_id'] = usuario.id 
    session['nombre'] = usuario.nombre 
    session['correo'] = usuario.correo

