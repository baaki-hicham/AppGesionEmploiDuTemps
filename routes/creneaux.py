from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.creneau import Creneau
from controllers.entity_controller import EntityController

creneaux_bp = Blueprint('creneaux', __name__, url_prefix='/creneaux')
controller = EntityController(Creneau)


@creneaux_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@creneaux_bp.route('/')
def index():
    query = request.args.get('q', '')
    creneaux = controller.list_all()
    if query:
        creneaux = [c for c in creneaux if query.lower() in f'{c.jour} {c.heure_debut} {c.heure_fin}'.lower()]
    return render_template('creneaux/index.html', creneaux=creneaux, query=query)


@creneaux_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        controller.create(
            jour=request.form.get('jour'),
            heure_debut=request.form.get('heure_debut'),
            heure_fin=request.form.get('heure_fin')
        )
        flash('Créneau ajouté.', 'success')
        return redirect(url_for('creneaux.index'))
    return render_template('creneaux/create.html')


@creneaux_bp.route('/edit/<int:creneau_id>', methods=['GET', 'POST'])
def edit(creneau_id):
    creneau = controller.get_by_id(creneau_id)
    if request.method == 'POST':
        controller.update(creneau,
                          jour=request.form.get('jour'),
                          heure_debut=request.form.get('heure_debut'),
                          heure_fin=request.form.get('heure_fin'))
        flash('Créneau mis à jour.', 'success')
        return redirect(url_for('creneaux.index'))
    return render_template('creneaux/edit.html', creneau=creneau)


@creneaux_bp.route('/delete/<int:creneau_id>', methods=['POST'])
def delete(creneau_id):
    creneau = controller.get_by_id(creneau_id)
    controller.delete(creneau)
    flash('Créneau supprimé.', 'success')
    return redirect(url_for('creneaux.index'))
