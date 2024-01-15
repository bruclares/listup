import functools
import psycopg
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash
from ..database.db import get_db
from ..models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        validation_errors = User.validate_login(request.form)

        if not validation_errors:
            user = User.login(request.form['email'])

            if user is None or not check_password_hash(user['password'], request.form['password']):
                flash('Dados incorretos', 'login_error')
            else:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('task.list'))

        for category, message in validation_errors.items():
            flash(message, category)

    return render_template('auth/login.html')


@bp.route('/cadastrar', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name'].title()
        password = request.form['password']
        email = request.form['email']

        error = None

        if not name:
            error = 'O nome é obrigatório.'
        elif not email:
            error = 'O email é obrigatório.'
        elif not password:
            error = 'A senha é obrigatória.'

        if error is None:
            try:
                User.register(name, email, password)
            except psycopg.IntegrityError:
                error = f"Já temos um usuário com o email {email}."
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

# vai executar a função antes de cada requisição 
# se usuario está logado, vai carregar as informações dele
@bp.before_app_request
def load_logged_in_user():
    User.logged_user()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
