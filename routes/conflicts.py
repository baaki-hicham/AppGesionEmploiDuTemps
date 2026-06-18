from flask import Blueprint, render_template, session, redirect, url_for
from services.conflict_service import ConflictDetector

conflicts_bp = Blueprint('conflicts', __name__, url_prefix='/conflicts')


@conflicts_bp.before_request
def auth_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))


@conflicts_bp.route('/')
def index():
    conflicts = ConflictDetector.detect_conflicts()
    return render_template('conflicts/index.html', conflicts=conflicts)
