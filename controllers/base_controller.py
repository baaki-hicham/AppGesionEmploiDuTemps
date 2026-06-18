from flask import flash


class BaseController:
    @staticmethod
    def commit_changes():
        from extensions import db
        try:
            db.session.commit()
            return True
        except Exception as exc:
            db.session.rollback()
            flash('Une erreur est survenue : ' + str(exc), 'danger')
            return False
