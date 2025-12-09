from .auth_routes import auth_bp
from .home_routes import home_bp
from .mail_routes import mail_bp
from .seguimiento_routes import seguimiento_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(mail_bp)
    app.register_blueprint(seguimiento_bp)
    