from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from ..database.db import get_db
from .auth_controller import login_required
from ..models.task import Task
from ..models.category import Category

bp = Blueprint('task', __name__, url_prefix='/tarefas')


@bp.route('/')
@login_required
def list():
    search = request.args.get('search')
    tasks = Task.get_all(search)

    if search and not tasks:
        tasks = 'Nenhuma tarefa encontrada...'

    return render_template('tarefas/list.html', tasks=tasks)


@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        user_id = session.get('user_id')
        description = request.form['description']
        category_id = request.form['category_id']

        error = None

        if not description:
            error = 'A tarefa é obrigatória.'

        if error is None:
            Task.insert(user_id, description, category_id)
            # url_for(nome do controller(bp).função)
            return redirect(url_for('task.list'))

        flash(error)

    #aqui eu pego as categorias e passo para o template
    categories = Category.get_all()

    return render_template('tarefas/create_task.html', categories=categories)


@bp.route('<id>/alterar', methods=('GET', 'POST'))
@login_required
def update(id):
    if request.method == 'POST':
        description = request.form['description']
        category_id = request.form['category_id']

        error = None

        if not description:
            error = 'A tarefa é obrigatória.'

        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        '''UPDATE tasks SET description = %s, category_id = %s
                        WHERE id = %s''',
                        (description, category_id, id))

            return redirect(url_for('task.list'))

        flash(error)

    # pego no banco tudo o que eu preciso para enviar ao formulário
    with get_db() as conn:
        with conn.cursor() as curs:
            # posso fazer todas as execuções no banco com o mesmo cursor
            # busco a tarefa
            curs.execute(
                'SELECT * FROM tasks WHERE id = %s',
                # parametro da função será o valor
                (id,)
            )
            task = curs.fetchone()

            # busco as categorias
            curs.execute('SELECT id, name FROM categories')
            categories = curs.fetchall()

    # envio com o forumulário tudo o que peguei do banco (task e categories)
    return render_template(
        'tarefas/update_task.html',
        task=task,
        categories=categories
    )


@bp.route('<id>/conclusao')
@login_required
def conclusion(id):
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                '''UPDATE tasks SET conclusion_date = CURRENT_TIMESTAMP
                WHERE id = %s''',
                (id,))
    return redirect(url_for('task.list'))


@bp.route('<id>/unconclude')
@login_required
def unconclude(id):
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                '''UPDATE tasks SET conclusion_date = NULL
                WHERE id = %s''',
                (id,))
    return redirect(url_for('task.list'))


@bp.route('/<id>/excluir')
@login_required
def delete(id):
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                'DELETE FROM tasks WHERE id = %s',
                (id,)
            )
    return redirect(url_for('task.list'))
