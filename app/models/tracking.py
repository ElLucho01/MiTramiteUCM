from app import db
from datetime import datetime

# Esta es la tabla de asociación que implementa el "Carrito" 
# y la lista de seguimiento [cite: 461]
class UserBenefitTracking(db.Model):
    __tablename__ = 'user_benefit_tracking'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.id'), primary_key=True)
    
    # Almacenamos el progreso y la fecha (del "Carrito") aquí
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    estado_progreso = db.Column(db.Float, default=0.0) # 

    # --- Relaciones ---
    user = db.relationship('User', back_populates='tracked_benefits')
    benefit = db.relationship('Benefit', back_populates='followers')

# Esta tabla almacena el estado 'cumplido'  de un requisito 
# para un usuario específico.
class UserRequirementStatus(db.Model):
    __tablename__ = 'user_requirement_status'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'), primary_key=True)
    
    cumplido = db.Column(db.Boolean, default=False, nullable=False) # 

    # --- Relaciones ---
    user = db.relationship('User', back_populates='requirement_statuses')
    requirement = db.relationship('Requirement', back_populates='user_statuses')