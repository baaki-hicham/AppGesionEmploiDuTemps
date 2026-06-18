from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.salle import Salle
from controllers.entity_controller import EntityController

salles_bp = Blueprint('salles', __name__, url_prefix='/salles')
controller = EntityController(Salle)


@salles_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@salles_bp.route('/')
def index():
    query = request.args.get('q', '')
    salles = controller.list_all()
    if query:
        salles = [s for s in salles if query.lower() in f'{s.nom} {s.type}'.lower()]
    return render_template('salles/index.html', salles=salles, query=query)


@salles_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        controller.create(
            nom=request.form.get('nom'),
            type=request.form.get('type'),
            capacite=int(request.form.get('capacite') or 0)
        )
        flash('Salle ajoutée.', 'success')
        return redirect(url_for('salles.index'))
    return render_template('salles/create.html')


@salles_bp.route('/edit/<int:salle_id>', methods=['GET', 'POST'])
def edit(salle_id):
    salle = controller.get_by_id(salle_id)
    if request.method == 'POST':
        controller.update(salle,
                          nom=request.form.get('nom'),
                          type=request.form.get('type'),
                          capacite=int(request.form.get('capacite') or 0))
        flash('Salle modifiée.', 'success')
        return redirect(url_for('salles.index'))
    return render_template('salles/edit.html', salle=salle)


@salles_bp.route('/delete/<int:salle_id>', methods=['POST'])
def delete(salle_id):
    salle = controller.get_by_id(salle_id)
    controller.delete(salle)
    flash('Salle supprimée.', 'success')
    return redirect(url_for('salles.index'))
