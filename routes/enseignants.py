from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import or_
from extensions import db
from models.enseignant import Enseignant
from controllers.entity_controller import EntityController

enseignants_bp = Blueprint('enseignants', __name__, url_prefix='/enseignants')
controller = EntityController(Enseignant)


@enseignants_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@enseignants_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    base_query = Enseignant.query
    if query:
        base_query = base_query.filter(
            or_(
                Enseignant.nom.ilike(f'%{query}%'),
                Enseignant.prenom.ilike(f'%{query}%'),
                Enseignant.email.ilike(f'%{query}%')
            )
        )
    pagination = controller.paginate(page=page, per_page=10, query=base_query)
    enseignants = pagination.items
    return render_template('enseignants/index.html', enseignants=enseignants, query=query, pagination=pagination)


@enseignants_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            'email': request.form.get('email'),
            'telephone': request.form.get('telephone'),
            'specialite': request.form.get('specialite'),
            'disponibilite': request.form.get('disponibilite')
        }
        controller.create(**data)
        flash('Enseignant ajouté avec succès.', 'success')
        return redirect(url_for('enseignants.index'))
    return render_template('enseignants/create.html')


@enseignants_bp.route('/edit/<int:enseignant_id>', methods=['GET', 'POST'])
def edit(enseignant_id):
    enseignant = controller.get_by_id(enseignant_id)
    if request.method == 'POST':
        controller.update(enseignant,
                          nom=request.form.get('nom'),
                          prenom=request.form.get('prenom'),
                          email=request.form.get('email'),
                          telephone=request.form.get('telephone'),
                          specialite=request.form.get('specialite'),
                          disponibilite=request.form.get('disponibilite'))
        flash('Enseignant modifié avec succès.', 'success')
        return redirect(url_for('enseignants.index'))
    return render_template('enseignants/edit.html', enseignant=enseignant)


@enseignants_bp.route('/delete/<int:enseignant_id>', methods=['POST'])
def delete(enseignant_id):
    enseignant = controller.get_by_id(enseignant_id)
    controller.delete(enseignant)
    flash('Enseignant supprimé.', 'success')
    return redirect(url_for('enseignants.index'))
