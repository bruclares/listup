import functools
import psycopg
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from ..database.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        if not email:
            error = 'O email é obrigatório.'
        elif not password:
            error = 'A senha é obrigatória.'

        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        'SELECT * FROM users WHERE email = %s',
                        (email,)
                    )
                    user = curs.fetchone()
        
        if user is None or not check_password_hash(user['password'], password):
            error = 'Dados incorretos'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('task.list'))
            

    if 'user_id' in session:
        return redirect(url_for('task.list'))

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
                with get_db() as conn:
                    with conn.cursor() as curs:
                        curs.execute(
                            '''INSERT INTO users (name, email, password)
                            VALUES (%s, %s, %s)''',
                            (name, email, generate_password_hash(password))
                        )
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
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    'SELECT * FROM users WHERE id = %s', (user_id,)
                )
                g.user = curs.fetchone()


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
