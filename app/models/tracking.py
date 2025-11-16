from . import db
from datetime import datetime

class Beneficios_Estado(db.Model):
    __tablename__ = 'beneficios_estado'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    benefit_id = db.Column(db.Integer, db.ForeignKey('beneficios.id'), nullable=False)
    
    # Almacenamos el progreso y la fecha (del "Carrito") aquí
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Float, default=0.0) # 

    # --- Relaciones ---
    user = db.relationship('User', back_populates='beneficios_estado')
    beneficios = db.relationship('Beneficios', back_populates='seguidores')

# Esta tabla almacena el estado 'cumplido'  de un requisito 
# para un usuario específico.
class Requerimientos_Estado(db.Model):
    __tablename__ = 'requerimientos_estado'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requerimientos.id'), nullable=False)
    
    cumplido = db.Column(db.Boolean, default=False, nullable=False) # 

    # --- Relaciones ---
    user = db.relationship('User', back_populates='requerimientos_estado')
    requerimientos = db.relationship('Requerimientos', back_populates='user_statuses')