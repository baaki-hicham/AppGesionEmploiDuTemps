from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models.matiere import Matiere
from controllers.entity_controller import EntityController

matieres_bp = Blueprint('matieres', __name__, url_prefix='/matieres')
controller = EntityController(Matiere)


@matieres_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@matieres_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    base_query = Matiere.query
    if query:
        base_query = base_query.filter(Matiere.nom.ilike(f'%{query}%'))
    pagination = controller.paginate(page=page, per_page=10, query=base_query)
    return render_template('matieres/index.html', matieres=pagination.items, query=query, pagination=pagination)


@matieres_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        controller.create(
            nom=request.form.get('nom'),
            volume_horaire=int(request.form.get('volume_horaire') or 0)
        )
        flash('Matière ajoutée.', 'success')
        return redirect(url_for('matieres.index'))
    return render_template('matieres/create.html')


@matieres_bp.route('/edit/<int:matiere_id>', methods=['GET', 'POST'])
def edit(matiere_id):
    matiere = controller.get_by_id(matiere_id)
    if request.method == 'POST':
        controller.update(matiere,
                          nom=request.form.get('nom'),
                          volume_horaire=int(request.form.get('volume_horaire') or 0))
        flash('Matière modifiée.', 'success')
        return redirect(url_for('matieres.index'))
    return render_template('matieres/edit.html', matiere=matiere)


@matieres_bp.route('/delete/<int:matiere_id>', methods=['POST'])
def delete(matiere_id):
    matiere = controller.get_by_id(matiere_id)
    controller.delete(matiere)
    flash('Matière supprimée.', 'success')
    return redirect(url_for('matieres.index'))
