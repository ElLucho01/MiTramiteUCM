# /app/models/notification.py
from . import db
from datetime import datetime

class Notificaciones(db.Model):
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50)) # 'email', 'app', etc.
    
    # Claves foráneas
    benefit_id = db.Column(db.Integer, db.ForeignKey('beneficios.id'), nullable=True) # Puede ser una notificación general

    # --- Relaciones ---
    usuarios_rel = db.relationship(
        'UserNotificaciones',
        back_populates='notificacion',
        cascade='all, delete-orphan'
    )

    beneficios = db.relationship('Beneficios', back_populates='notificaciones')

    def __repr__(self):
        return f'<Notification {self.id}>'
    

class UserNotificaciones(db.Model):
    __tablename__ = 'user_notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notificacion_id = db.Column(db.Integer, db.ForeignKey('notificaciones.id'), nullable=False)

    # Campos adicionales por usuario
    leido = db.Column(db.Boolean, default=False)
    fecha_recibida = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones inversas
    user = db.relationship('User', back_populates='notificaciones_rel')
    notificacion = db.relationship('Notificaciones', back_populates='usuarios_rel')

    def __repr__(self):
        return f'<UserNotificación user={self.user_id} notif={self.notificacion_id}>'