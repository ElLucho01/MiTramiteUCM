from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from models import db  # Importa la instancia de SQLAlchemy desde models/__init__.py
from models.user import User
from models.benefit import Beneficios, Requerimientos
from models.tracking import Beneficios_Estado
from flask_mail import Mail
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
import os
from utils import tracking_loader

mail = Mail()
scheduler = APScheduler()

def beneficios_usuario(user_id):
    if not user_id:
        return []

    beneficios = (
        Beneficios_Estado.query
        .filter_by(user_id=user_id)
        .join(Beneficios_Estado.beneficios)
        .all()
    )
    return beneficios

def registrar_hooks(app):

    @app.before_request
    def cargar_beneficios_en_g():
        user_id = session.get("user_id")
        g.beneficios_usuario = beneficios_usuario(user_id)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tracking_loader)
    registrar_hooks(app)
    
    #Configuración de Flask-Mail
    load_dotenv("VariablesNotifications.env")
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "true"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "true"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()


    # Configuración de la base de datos
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:postgres@db:5432/mitramiteucm_2'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave-secreta-super-segura'

    # Inicializar la base de datos con Flask
    db.init_app(app)

    # Registrar blueprints (rutas)
    from routes import register_routes
    register_routes(app)

    # Crear tablas dentro del contexto de la app
    with app.app_context():
        print("🔧 Creando tablas si no existen...")
        db.create_all()
        print("✅ Tablas verificadas / creadas.")

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
