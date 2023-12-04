from flask import (
    Blueprint, render_template, request, redirect, url_for, g, flash
)

from .auth_views import login_required
from .models import Todo
from . import db

bp = Blueprint('todo_views', __name__, url_prefix='/todo')

@bp.route('/list')
@login_required # decorator: authentication middleware
def index():
    todos = Todo.query.order_by(Todo.id.desc()).filter(Todo.created_by == g.user.id).all()

    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        todo = Todo(g.user.id, title, description)
        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('todo_views.index'))

    return render_template('todo/create.html')

def get_todo_by_id(id):
    return Todo.query.get_or_404(id)

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo_by_id(id)
    if request.method == 'POST':
        todo.title = request.form['title'].strip()
        todo.description = request.form['description'].strip()
        todo.status = True if request.form.get('status') == 'on' else False
        
        db.session.commit()

        message = {
            'message': 'Task successfully updated!!',
            'type': 'alert-success'
        }
        flash(message)

        return redirect(url_for('todo_views.index'))

    return render_template('todo/update.html', todo = todo)

@bp.route('/delete/<int:id>', methods=["DELETE"])
@login_required
def delete(id):
    db.session.delete(get_todo_by_id(id))
    db.session.commit()
    
    return ''

