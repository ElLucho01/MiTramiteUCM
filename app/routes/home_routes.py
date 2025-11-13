from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db
from models.benefit import Beneficios, Requerimientos
from utils import login_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@login_required
def home():
    beneficios = Beneficios.query.all()
    return render_template('home.html', usuario=session.get('user_id'), beneficios=beneficios)

@home_bp.route('/beneficio/<int:beneficio_id>')
def beneficio_detail(beneficio_id):
    beneficio = Beneficios.query.get_or_404(beneficio_id)
    return render_template('beneficio.html', beneficio=beneficio)

@home_bp.route('/requerimientos/<int:beneficio_id>')
def requerimiento_detail(beneficio_id):
    beneficio = Beneficios.query.get_or_404(beneficio_id)
    requerimientos = Requerimientos.query.filter_by(beneficio_id=beneficio_id).all()
    return render_template('requerimientos.html', beneficio=beneficio, requerimientos=requerimientos)
    
