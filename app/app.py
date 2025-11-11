from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db  # Importa la instancia de SQLAlchemy desde models/__init__.py
from routes import routes_bp
import os

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:postgres@db:5432/mitramiteucm_2'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave-secreta-super-segura'

    # Inicializar la base de datos con Flask
    db.init_app(app)

    # Registrar blueprints (rutas)
    app.register_blueprint(routes_bp)

    # Crear tablas dentro del contexto de la app
    with app.app_context():
        print("🔧 Creando tablas si no existen...")
        db.create_all()
        print("✅ Tablas verificadas / creadas.")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
