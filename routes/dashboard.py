from flask import Blueprint, render_template, session
from services.statistics_service import StatisticsService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
def index():
    stats = {
        'enseignants': StatisticsService.count_enseignants(),
        'classes': StatisticsService.count_classes(),
        'matieres': StatisticsService.count_matieres(),
        'salles': StatisticsService.count_salles(),
        'seances': StatisticsService.count_seances()
    }
    chart_data = {
        'salles': StatisticsService.occupation_salles(),
        'enseignants': StatisticsService.occupation_enseignants(),
        'matieres': StatisticsService.volume_horaire_par_matiere()
    }
    return render_template('dashboard/index.html', stats=stats, chart_data=chart_data)
