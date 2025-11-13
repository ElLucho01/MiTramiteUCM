# /app/models/benefit_event.py
from app import db
from datetime import datetime

class Evento_Beneficio(db.Model):
    __tablename__ = 'eventos_beneficio'
    
    id = db.Column(db.Integer, primary_key=True)
    beneficio_id = db.Column(db.Integer, db.ForeignKey('beneficios.id'), nullable=False)
    
    # Ej: 'Inicio Postulación', 'Resultados', 'Fecha Límite'
    nombre = db.Column(db.String(200), nullable=False)
    
    fecha = db.Column(db.Date, nullable=False) # Usamos Date, no DateTime

    # --- Relaciones ---
    beneficio = db.relationship('Beneficios', back_populates='eventos')

    def __repr__(self):
        return f'<BenefitEvent {self.nombre} - {self.fecha}>'