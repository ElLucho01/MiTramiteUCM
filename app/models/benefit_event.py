# /app/models/benefit_event.py
from . import db
from datetime import datetime

class Evento_Beneficio(db.Model):
    __tablename__ = 'eventos_beneficio'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Ej: 'Inicio Postulación', 'Resultados', 'Fecha Límite'
    nombre = db.Column(db.String(200), nullable=False)
    
    fecha = db.Column(db.Date, nullable=False) # Usamos Date, no DateTime


    def __repr__(self):
        return f'<BenefitEvent {self.nombre} - {self.fecha}>'
    
    