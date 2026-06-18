from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import or_
from extensions import db
from models.classe import Classe
from controllers.entity_controller import EntityController

classes_bp = Blueprint('classes', __name__, url_prefix='/classes')
controller = EntityController(Classe)


@classes_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@classes_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    base_query = Classe.query
    if query:
        base_query = base_query.filter(
            or_(Classe.nom.ilike(f'%{query}%'), Classe.niveau.ilike(f'%{query}%'))
        )
    pagination = controller.paginate(page=page, per_page=10, query=base_query)
    return render_template('classes/index.html', classes=pagination.items, query=query, pagination=pagination)


@classes_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        controller.create(
            nom=request.form.get('nom'),
            niveau=request.form.get('niveau'),
            effectif=int(request.form.get('effectif') or 0)
        )
        flash('Classe créée avec succès.', 'success')
        return redirect(url_for('classes.index'))
    return render_template('classes/create.html')


@classes_bp.route('/edit/<int:classe_id>', methods=['GET', 'POST'])
def edit(classe_id):
    classe = controller.get_by_id(classe_id)
    if request.method == 'POST':
        controller.update(classe,
                          nom=request.form.get('nom'),
                          niveau=request.form.get('niveau'),
                          effectif=int(request.form.get('effectif') or 0))
        flash('Classe mise à jour.', 'success')
        return redirect(url_for('classes.index'))
    return render_template('classes/edit.html', classe=classe)


@classes_bp.route('/delete/<int:classe_id>', methods=['POST'])
def delete(classe_id):
    classe = controller.get_by_id(classe_id)
    controller.delete(classe)
    flash('Classe supprimée.', 'success')
    return redirect(url_for('classes.index'))
