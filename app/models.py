from app import db

#Modelo de Base de Datos de Usuarios
# Tabla: usuarios

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
