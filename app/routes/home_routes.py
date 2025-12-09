from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import db
from models.benefit import Beneficios, Requerimientos
from models.tracking import Beneficios_Estado
from utils import login_required

home_bp = Blueprint('home', __name__)

#Mostramos la página de inicio con los beneficios
@home_bp.route('/')
def home():
    beneficios = Beneficios.query.all()
    user_id = session.get('user_id') if 'user_id' in session else None
    return render_template('home.html', usuario=user_id, beneficios=beneficios)

#Mostramos el beneficio y la descripción de este
@home_bp.route('/beneficio/<int:beneficio_id>')
def beneficio_detail(beneficio_id):
    beneficio = Beneficios.query.get_or_404(beneficio_id)
    siguiendo = Beneficios_Estado.query.filter_by(user_id=session.get('user_id'), benefit_id=beneficio_id).first() is not None
    return render_template('beneficio.html', beneficio=beneficio, siguiendo=siguiendo)

#Mostramos los detalles de los requerimientos de un beneficio
@home_bp.route('/requerimientos/<int:beneficio_id>')
@login_required
def requerimiento_detail(beneficio_id):
    beneficio = Beneficios.query.get_or_404(beneficio_id)
    requerimientos = Requerimientos.query.filter_by(beneficio_id=beneficio_id).all()
    reqs = []
    for r in requerimientos:
        partes = parse_requerimiento(r.descripcion)
        reqs.append({
        "id": r.id,
        "nombre": r.nombre,
        "que": partes["que"],
        "como": partes["como"],      # lista de pasos
        "donde": partes["donde"]
    })
    return render_template('requerimientos.html', beneficio=beneficio, requerimientos=reqs)


#Se realiza la busqueda de beneficios con la barra superior
@home_bp.route('/busqueda', methods=['GET'])
def busqueda():
    query = request.args.get('q', '')
    if not query:
        return jsonify({})
    beneficio = Beneficios.query.filter(Beneficios.nombre.ilike(f'%{query}%')).all()
    return jsonify([
        {'id': beneficio.id,
        'nombre': beneficio.nombre}
        for beneficio in beneficio
    ])

@home_bp.route('/recomendaciones')
def recomendaciones():
    return render_template('recomendaciones.html')
        
#Se arregla el formato de descripción de los requerimientos
def parse_requerimiento(texto):

    partes = texto.split(".")
    partes = [p.strip() for p in partes if p.strip()]  # limpiar vacíos


    que = partes[0]
    como = partes[1]
    donde = partes[2]

    # Los pasos del "cómo" están separados por |
    pasos_como = [p.strip() for p in como.split("|") if p.strip()]

    return {
        "que": que,
        "como": pasos_como,
        "donde": donde
    }

    
