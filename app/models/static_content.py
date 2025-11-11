# /app/models/static_content.py
from app import db
from datetime import datetime

class StaticContent(db.Model):
    __tablename__ = 'static_content'
    
    # Usamos una 'clave' (ej: 'ayuda', 'contacto') para identificar la página
    id = db.Column(db.String(50), primary_key=True) 
    
    # El contenido HTML o Markdown que el admin edita
    content = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<StaticContent {self.id}>'