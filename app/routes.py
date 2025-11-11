from flask import Blueprint, render_template, request, redirect, url_for

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def log_user():
    return render_template('login.html')

@routes_bp.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    print(f"Usuario registrado: {nombre} - {correo}")
    return redirect(url_for('routes.home'))

@routes_bp.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    print(f"Inicio de sesión: {correo}")
    return redirect(url_for('routes.home'))

@routes_bp.route('/home')
def home():
    return render_template('home.html')
