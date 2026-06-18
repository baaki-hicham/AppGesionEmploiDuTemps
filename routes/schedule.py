from flask import Blueprint, render_template, redirect, url_for, flash, session
from services.schedule_service import ScheduleGenerator
from models.seance import Seance

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@schedule_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@schedule_bp.route('/')
def index():
    seances = Seance.query.order_by(Seance.creneau_id).all()
    return render_template('schedule/index.html', seances=seances)


@schedule_bp.route('/generate')
def generate():
    generator = ScheduleGenerator()
    generator.generate()
    flash('Génération de l emploi du temps terminée.', 'success')
    return redirect(url_for('schedule.index'))
