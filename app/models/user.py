from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
        
    notificaciones_rel = db.relationship(
        'UserNotificaciones',
        back_populates='user',
        cascade='all, delete-orphan'
    )    

    beneficios_estado = db.relationship('Beneficios_Estado', back_populates='user', cascade='all, delete-orphan')
    
    requerimientos_estado = db.relationship('Requerimientos_Estado', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.correo}>'