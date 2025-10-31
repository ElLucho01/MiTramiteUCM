from flask import Blueprint, jsonify
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Conexión Flask-PostgreSQL funcionando correctamente"})
