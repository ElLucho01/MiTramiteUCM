from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from models.user import User
from utils import login_required
from flask import make_response



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
        return redirect(url_for('auth.index'))
    usuario = User(nombre=nombre, correo=correo)
    usuario.set_password(contrasena)
    #Se añade el usuario a la base de datos
    db.session.add(usuario)
    db.session.commit()
    #Se registra la información en la sesión
    log_user(usuario)
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
        return redirect(url_for('auth.index'))
    
#Cerrar Sesión
@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home.home'))

#Se cargan los datos del usuario en la sesión
def log_user(usuario):
    session['user_id'] = usuario.id 
    session['nombre'] = usuario.nombre 
    session['correo'] = usuario.correo

