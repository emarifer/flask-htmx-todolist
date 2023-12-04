from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g,
)

from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

bp = Blueprint('auth_views', __name__, url_prefix='/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(username, generate_password_hash(password))

        message = {}

        user_name = User.query.filter_by(username=username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()

            message = {
                'message': 'You have successfully registered',
                'type': 'alert-success'
            }
            flash(message)

            return redirect(url_for('auth_views.login'))
        else:
            message = {
                'message': f'The user «{username}» is already registered',
                'type': 'alert-error'
            }

        flash(message)

    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        message: dict[str, str] = None

        # Validate data
        user: User = User.query.filter_by(username = username).first()
        # The correct thing to do would be to send a single,
        # non-specific error message.
        if user == None:
            message = {
                'message': 'Incorrect username',
                'type': 'alert-error'
            }
            
        elif not check_password_hash(user.password, password):
            message = {
                'message': 'Incorrect password',
                'type': 'alert-error'
            }

        # Log In
        if message is None:
            session.clear() # clean the session, in case there is one started
            session['user_id'] = user.id

            message = {
                'message': 'You have successfully logged in!!',
                'type': 'alert-success'
            }
            flash(message)

            return redirect(url_for('todo_views.index'))

        flash(message)

    return render_template('auth/login.html')

@bp.before_app_request # runs on every request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
        # Get the user from the database or return a 404 error

@bp.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('index'))


# functools allows us to generate decorator functions
import functools

# Similar to authentication middleware
def login_required(view): # "view" are the views or route controllers
    @functools.wraps(view)
    def wrapped_view(**kwargs): # **kwargs are the view arguments
        if g.user is None:            
            return redirect(url_for('auth_views.login'))
        
        # lets the view pass, that is, executes the controller or route handler
        return view(**kwargs)
    
    return wrapped_view