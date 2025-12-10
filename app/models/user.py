from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
        
    # --- RELACIONES (Estas son las que faltaban o daban error) ---
    notificaciones_rel = db.relationship(
        'UserNotificaciones',
        back_populates='user',
        cascade='all, delete-orphan'
    )    

    beneficios_estado = db.relationship(
        'Beneficios_Estado', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    
    requerimientos_estado = db.relationship(
        'Requerimientos_Estado', 
        back_populates='user'
    )

    # --- MÉTODOS DE CONTRASEÑA ---

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- NUEVOS MÉTODOS PARA RECUPERACIÓN (Token) ---

    def get_reset_token(self):
        # Genera un token serializado que contiene el ID del usuario
        s = Serializer(current_app.config['SECRET_KEY'])
        # El 'salt' diferencia este token de otros usos
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, expiration=3600):
        # expiration: tiempo en segundos (3600 = 1 hora)
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='password-reset-salt', max_age=expiration)
            user_id = data['user_id']
        except:
            return None
        
        # Usamos db.session.get para SQLAlchemy 2.0+
        return db.session.get(User, user_id)

    def __repr__(self):
        return f'<User {self.correo}>'