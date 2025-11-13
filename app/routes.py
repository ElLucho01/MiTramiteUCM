from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.user import User

routes_bp = Blueprint('routes', __name__)

#Al abrir la pagina principal
@routes_bp.route('/')
def index():
    return render_template('login.html')

 #En caso de pulsar el boton de registrar
@routes_bp.route('/registrar', methods=['POST'])
def registrar():
    #Se registran los datos del formulario de registro
    nombre = request.form.get('nombreReg')
    correo = request.form.get('correoReg')
    contrasena = request.form.get('contrasenaReg')
    #Se comprueba que el correo no esté ya registrado

    usuario = User.query.filter_by(correo=correo).first()
    if usuario:
        #En caso de que el usuario ya esté registrado, se redirige a la página principal (agregar mensaje de error)
        return redirect(url_for('routes.index'))
    #Se introduce al usuario a la db y se redirige a la página de inicio
    usuario = User(nombre=nombre, correo=correo)
    usuario.set_password(contrasena)
    db.session.add(usuario)
    db.session.commit()
    print(f"Usuario registrado: {correo}")
    return redirect(url_for('routes.home'))

@routes_bp.route('/login', methods=['POST'])
def login():
    correo = request.form.get('correoLog')
    contrasena = request.form.get('contrasenaLog')
    usuario = User.query.filter_by(correo=correo).first()
    if usuario and usuario.check_password(contrasena):
        #Login exitoso, redirigir a la página de inicio
        print(f"Usuario logueado: {correo}")
        return redirect(url_for('routes.home'))
    else:
        #Login fallido, redirigir a la página principal (agregar mensaje de error)
        return redirect(url_for('routes.index'))


@routes_bp.route('/home')
def home():
    return render_template('home.html')
