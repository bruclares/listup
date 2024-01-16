from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
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
        category_id = request.form['category_id']
        validation_errors = Task.validate(request.form)

        if not validation_errors:
            Task.insert(user_id, request.form['description'], category_id)
            # url_for(nome do controller(bp).função)
            return redirect(url_for('task.list'))

        for category, message in validation_errors.items():
            flash(message, category)

    # aqui eu pego as categorias e passo para o template
    categories = Category.get_all()

    return render_template('tarefas/create_task.html', categories=categories)


@bp.route('<id>/alterar', methods=('GET', 'POST'))
@login_required
def edit(id):
    if request.method == 'POST':
        category_id = request.form['category_id']
        validation_errors = Task.validate(request.form)

        if not validation_errors:
            Task.update(request.form['description'], category_id, id)

            return redirect(url_for('task.list'))

        for category, message in validation_errors.items():
            flash(message, category)

    task = Task.get_from_id(id)

    categories = Category.get_all()

    return render_template(
        'tarefas/update_task.html',
        task=task,
        categories=categories
    )


@bp.route('<id>/conclusao')
@login_required
def conclusion(id):
    Task.check(id)

    return redirect(url_for('task.list'))


@bp.route('<id>/unconclude')
@login_required
def unconclude(id):
    Task.uncheck(id)

    return redirect(url_for('task.list'))


@bp.route('/<id>/excluir')
@login_required
def delete(id):
    Task.delete(id)

    return redirect(url_for('task.list'))
