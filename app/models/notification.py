# /app/models/notification.py
from . import db
from datetime import datetime

class Notificaciones(db.Model):
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tipo = db.Column(db.String(50)) # 'email', 'app', etc.
    leido = db.Column(db.Boolean, default=False)
    
    # Claves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    benefit_id = db.Column(db.Integer, db.ForeignKey('beneficios.id'), nullable=True) # Puede ser una notificación general

    # --- Relaciones ---
    user = db.relationship('User', back_populates='notificaciones')
    benefit = db.relationship('Beneficio', back_populates='notificaciones')

    def __repr__(self):
        return f'<Notification {self.id}>'