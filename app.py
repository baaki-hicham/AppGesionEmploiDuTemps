import os
from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from extensions import db, csrf

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(basedir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from models import base
        from models.user import User
        from models.enseignant import Enseignant
        from models.classe import Classe
        from models.matiere import Matiere
        from models.salle import Salle
        from models.creneau import Creneau
        from models.seance import Seance

        db.create_all()
        init_default_admin(app)

    register_blueprints(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app


def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.enseignants import enseignants_bp
    from routes.classes import classes_bp
    from routes.matieres import matieres_bp
    from routes.salles import salles_bp
    from routes.creneaux import creneaux_bp
    from routes.seances import seances_bp
    from routes.schedule import schedule_bp
    from routes.conflicts import conflicts_bp
    from routes.exports import exports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(enseignants_bp)
    app.register_blueprint(classes_bp)
    app.register_blueprint(matieres_bp)
    app.register_blueprint(salles_bp)
    app.register_blueprint(creneaux_bp)
    app.register_blueprint(seances_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(conflicts_bp)
    app.register_blueprint(exports_bp)


def init_default_admin(app):
    from services.auth_service import AuthService
    from models.user import User

    admin_email = 'admin@ecole.com'
    if not User.query.filter_by(email=admin_email).first():
        password = AuthService.hash_password('Admin2026!')
        admin = User(nom='Admin', prenom='Systeme', email=admin_email, password=password, role='Admin')
        db.session.add(admin)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
