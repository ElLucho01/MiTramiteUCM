# /app/models/benefit_event.py
from app import db
from datetime import datetime

class BenefitEvent(db.Model):
    __tablename__ = 'benefit_events'
    
    id = db.Column(db.Integer, primary_key=True)
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.id'), nullable=False)
    
    # Ej: 'Inicio Postulación', 'Resultados', 'Fecha Límite'
    name = db.Column(db.String(200), nullable=False)
    
    event_date = db.Column(db.Date, nullable=False) # Usamos Date, no DateTime

    # --- Relaciones ---
    benefit = db.relationship('Benefit', back_populates='events')

    def __repr__(self):
        return f'<BenefitEvent {self.name} - {self.event_date}>'