# /app/models/benefit.py
from app import db
from datetime import datetime

class Benefit(db.Model):
    __tablename__ = 'benefits'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=False)
    
    # La 'fuente' y 'fechaActualizacion' [cite: 186] del scraping 
    # tienen más sentido aquí que en una tabla separada.
    fuente = db.Column(db.String(100))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # --- Relaciones ---
    
    # 1-a-Muchos: Un beneficio tiene muchos requisitos
    requirements = db.relationship('Requirement', back_populates='benefit', 
                                   cascade="all, delete-orphan")
    
    # 1-a-Muchos: Un beneficio puede generar muchas notificaciones
    notifications = db.relationship('Notification', back_populates='benefit')
    
    # Muchos-a-Muchos: Un beneficio puede ser seguido por muchos usuarios
    followers = db.relationship('UserBenefitTracking', back_populates='benefit')

    def __repr__(self):
        return f'<Benefit {self.nombre}>'

class Requirement(db.Model):
    __tablename__ = 'requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    
    # Clave foránea para la relación 1-a-Muchos
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.id'), nullable=False)
    
    # --- Relaciones ---
    benefit = db.relationship('Benefit', back_populates='requirements')
    
    # Muchos-a-Muchos: Un requisito puede tener un estado para muchos usuarios
    user_statuses = db.relationship('UserRequirementStatus', back_populates='requirement')

    def __repr__(self):
        return f'<Requirement {self.descripcion[:30]}>'