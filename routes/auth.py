from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from models.user import User
from extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = AuthService.authenticate(email, password)
        if user:
            session['user_id'] = user.id
            session['user_name'] = f'{user.prenom} {user.nom}'
            session['user_role'] = user.role
            flash('Connexion réussie.', 'success')
            return redirect(url_for('dashboard.index'))
        flash('Identifiants invalides.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('auth.login'))
