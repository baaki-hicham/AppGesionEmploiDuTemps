import os
from flask import Blueprint, send_file, redirect, url_for, flash, session
from services.export_service import ExportService
from config import Config

exports_bp = Blueprint('exports', __name__, url_prefix='/exports')


@exports_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@exports_bp.route('/excel')
def excel():
    filename = 'emploi_du_temps.xlsx'
    path = ExportService.generate_excel(filename)
    return send_file(path, as_attachment=True)


@exports_bp.route('/pdf')
def pdf():
    filename = 'emploi_du_temps.pdf'
    path = ExportService.generate_pdf(filename)
    return send_file(path, as_attachment=True)


@exports_bp.route('/backup')
def backup():
    db_path = os.path.join(Config().EXPORT_FOLDER, 'backup_database.db')
    if os.path.exists(Config().SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')):
        from shutil import copyfile
        copyfile(Config().SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''), db_path)
        flash('Backup SQLite créé.', 'success')
    else:
        flash('Aucune base de données trouvée.', 'danger')
    return redirect(url_for('dashboard.index'))
