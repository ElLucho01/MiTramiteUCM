from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar todos los modelos para que SQLAlchemy los registre
from .user import User
from .static_content import StaticContent
from .benefit import Beneficios, Requerimientos
from .tracking import Beneficios_Estado, Requerimientos_Estado
from .notification import Notificaciones
from .benefit_event import Evento_Beneficio
from .scraping_logs import ScrapingLog
