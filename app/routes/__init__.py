from .auth_routes import auth_bp
from .home_routes import home_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    