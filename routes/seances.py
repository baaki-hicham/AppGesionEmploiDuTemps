from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.seance import Seance
from models.classe import Classe
from models.enseignant import Enseignant
from models.matiere import Matiere
from models.salle import Salle
from models.creneau import Creneau
from controllers.entity_controller import EntityController

seances_bp = Blueprint('seances', __name__, url_prefix='/seances')
controller = EntityController(Seance)


@seances_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@seances_bp.route('/')
def index():
    classes = Classe.query.all()
    enseignants = Enseignant.query.all()
    matieres = Matiere.query.all()
    salles = Salle.query.all()
    creneaux = Creneau.query.all()

    query = request.args.get('q', '')
    seances = controller.list_all()
    if query:
        seances = [s for s in seances if query.lower() in f'{s.classe.nom} {s.enseignant.nom} {s.matiere.nom} {s.salle.nom}'.lower()]
    return render_template('seances/index.html', seances=seances, classes=classes, enseignants=enseignants, matieres=matieres, salles=salles, creneaux=creneaux, query=query)


@seances_bp.route('/create', methods=['GET', 'POST'])
def create():
    classes = Classe.query.all()
    enseignants = Enseignant.query.all()
    matieres = Matiere.query.all()
    salles = Salle.query.all()
    creneaux = Creneau.query.all()
    if request.method == 'POST':
        controller.create(
            classe_id=int(request.form.get('classe_id')),
            enseignant_id=int(request.form.get('enseignant_id')),
            matiere_id=int(request.form.get('matiere_id')),
            salle_id=int(request.form.get('salle_id')),
            creneau_id=int(request.form.get('creneau_id'))
        )
        flash('Séance créée.', 'success')
        return redirect(url_for('seances.index'))
    return render_template('seances/create.html', classes=classes, enseignants=enseignants, matieres=matieres, salles=salles, creneaux=creneaux)


@seances_bp.route('/edit/<int:seance_id>', methods=['GET', 'POST'])
def edit(seance_id):
    seance = controller.get_by_id(seance_id)
    classes = Classe.query.all()
    enseignants = Enseignant.query.all()
    matieres = Matiere.query.all()
    salles = Salle.query.all()
    creneaux = Creneau.query.all()
    if request.method == 'POST':
        controller.update(seance,
                          classe_id=int(request.form.get('classe_id')),
                          enseignant_id=int(request.form.get('enseignant_id')),
                          matiere_id=int(request.form.get('matiere_id')),
                          salle_id=int(request.form.get('salle_id')),
                          creneau_id=int(request.form.get('creneau_id')))
        flash('Séance mise à jour.', 'success')
        return redirect(url_for('seances.index'))
    return render_template('seances/edit.html', seance=seance, classes=classes, enseignants=enseignants, matieres=matieres, salles=salles, creneaux=creneaux)


@seances_bp.route('/delete/<int:seance_id>', methods=['POST'])
def delete(seance_id):
    seance = controller.get_by_id(seance_id)
    controller.delete(seance)
    flash('Séance supprimée.', 'success')
    return redirect(url_for('seances.index'))
