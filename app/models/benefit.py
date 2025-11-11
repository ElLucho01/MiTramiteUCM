# /app/models/benefit.py
from . import db
from datetime import datetime

class Beneficios(db.Model):
    __tablename__ = 'beneficios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=False)
    
    # La 'fuente' y 'fechaActualizacion' [cite: 186] del scraping 
    # tienen más sentido aquí que en una tabla separada.
    fuente = db.Column(db.String(100))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # --- Relaciones ---
    
    # 1-a-Muchos: Un beneficio tiene muchos requisitos
    requirements = db.relationship('Requerimiento', back_populates='beneficios', 
                                   cascade="all, delete-orphan")
    
    # 1-a-Muchos: Un beneficio puede generar muchas notificaciones
    notifications = db.relationship('Notificaciones', back_populates='beneficios')
    
    # Muchos-a-Muchos: Un beneficio puede ser seguido por muchos usuarios
    followers = db.relationship('Beneficios_Estado', back_populates='beneficios')

    def __repr__(self):
        return f'<Benefit {self.nombre}>'

class Requerimientos(db.Model):
    __tablename__ = 'requerimientos'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    
    # Clave foránea para la relación 1-a-Muchos
    benefit_id = db.Column(db.Integer, db.ForeignKey('beneficios.id'), nullable=False)
    
    # --- Relaciones ---
    benefit = db.relationship('Beneficios', back_populates='requerimientos')
    
    # Muchos-a-Muchos: Un requisito puede tener un estado para muchos usuarios
    user_statuses = db.relationship('Requerimientos_Estado', back_populates='requerimientos')

    def __repr__(self):
        return f'<Requerimiento {self.descripcion[:30]}>'