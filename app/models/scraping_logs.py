# /app/models/scraping_log.py
from . import db
from datetime import datetime

class ScrapingLog(db.Model):
    __tablename__ = 'scraping_log'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    # 'MINEDUC', 'UCM'
    source = db.Column(db.String(100), nullable=False) 
    
    # 'success', 'failure', 'unavailable'
    status = db.Column(db.String(20), nullable=False) 
    
    # Mensaje de éxito o error
    message = db.Column(db.Text, nullable=True) 
    
    # Cuántos beneficios se encontraron/actualizaron
    records_updated = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ScrapingLog {self.timestamp} - {self.status}>'