from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from ..database.db import get_db
from .auth_controller import login_required

bp = Blueprint('task', __name__, url_prefix='/tarefas')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def list():
    user_id = session.get('user_id')
    query = 'SELECT * FROM tasks WHERE user_id = %s'
    parameters = (user_id,)

    search = request.args.get('search')
    if search:
        query += ' and description ilike %s'
        parameters += ('%' + (search if search else '') + '%',)
      
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                query,
                parameters
            )
            tasks = curs.fetchall()
    
    if search and not tasks:
        tasks = 'Nenhuma tarefa encontrada...'
    
    return render_template('tarefas/list.html', tasks=tasks)


@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        user_id = session.get('user_id')
        description = request.form['description'].capitalize()
        category_id = request.form['category_id']

        error = None

        if not description:
            error = 'A tarefa é obrigatória.'

        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        '''INSERT INTO tasks (user_id, description,
                        category_id) VALUES(%s, %s, %s)''',
                        (user_id, description, category_id))
            
            # url_for(nome do controller(bp).função)
            return redirect(url_for('task.list'))
        
        flash(error)

    return render_template('tarefas/create_task.html')

