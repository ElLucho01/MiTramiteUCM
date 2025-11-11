from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos los modelos para que SQLAlchemy los registre
from .user import User
from .static_content import StaticContent
from .tracking import Beneficio_Estado, Requerimiento_Estado
from .benefit import Beneficios, Requerimientos
from .notification import Notificaciones
from .benefit_event import Evento_Beneficio
from .scraping_logs import ScrapingLog
