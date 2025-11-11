from . import db
from datetime import datetime

class Beneficio_Estado(db.Model):
    __tablename__ = 'beneficio_estado'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('beneficios.id'), primary_key=True)
    
    # Almacenamos el progreso y la fecha (del "Carrito") aquí
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    estado_progreso = db.Column(db.Float, default=0.0) # 

    # --- Relaciones ---
    user = db.relationship('User', back_populates='tracked_benefits')
    benefit = db.relationship('Benefit', back_populates='followers')

# Esta tabla almacena el estado 'cumplido'  de un requisito 
# para un usuario específico.
class Requerimiento_Estado(db.Model):
    __tablename__ = 'requerimientos_estado'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requerimientos.id'), primary_key=True)
    
    cumplido = db.Column(db.Boolean, default=False, nullable=False) # 

    # --- Relaciones ---
    user = db.relationship('User', back_populates='requirement_statuses')
    requirement = db.relationship('Requerimientos', back_populates='user_statuses')