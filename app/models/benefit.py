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
        
    # 1-a-Muchos: Un beneficio puede generar muchas notificaciones
    notificaciones = db.relationship('Notificaciones', back_populates='beneficios')
    
    # Muchos-a-Muchos: Un beneficio puede ser seguido por muchos usuarios
    seguidores = db.relationship('Beneficios_Estado', back_populates='beneficios', cascade='all, delete-orphan')
    

    def __repr__(self):
        return f'<Benefit {self.nombre}>'

class Requerimientos(db.Model):
    __tablename__ = 'requerimientos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    pasos = db.Column(db.Text, nullable=True)
        
    # --- Relaciones ---
    
    # Muchos-a-Muchos: Un requisito puede tener un estado para muchos usuarios
    user_statuses = db.relationship('Requerimientos_Estado', back_populates='requerimientos')

    def __repr__(self):
        return f'<Requerimiento {self.descripcion[:30]}>'