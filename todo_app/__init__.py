from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize the extension SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="assets") # Ver Nota 1 abajo

    # Project settings
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'd9d3e93eead4ddaa24436a0ed3b1dc6f47cbb9207b9b8ebd',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app_data.db'
    )

    # initialize the app with the extension SQLAlchemy
    db.init_app(app)

    # Registering Blueprints
    from . import todo_views # The dot (".") is the current package
    app.register_blueprint(todo_views.bp)

    from . import auth_views
    app.register_blueprint(auth_views.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    # To create the tables schemas in the database:
    # migrate application models
    with app.app_context():
        db.create_all()
    
    return app







""" REFERENCES:
https://www.youtube.com/watch?v=BetOsz7aCbU
https://github.com/alexroel/todo-list-flask

https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask

'd9d3e93eead4ddaa24436a0ed3b1dc6f47cbb9207b9b8ebd'

flask --app todo_app --debug run

[Nota 1] - Enlaces Inteligentes en Flask con url_for (permiten cambiar nombres de carpetas en un solo lugar):
https://www.youtube.com/watch?v=qMeCTF-Dm90

https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
https://soumendrak.medium.com/autoincrement-id-support-in-sqlalchemy-6a1383520ce3

https://www.digitalocean.com/community/tutorials/python-str-repr-functions
https://www.educative.io/answers/what-is-the-repr-method-in-python

Flask Shell. VER:
https://youtu.be/BetOsz7aCbU?si=RhqpmfzD6sliI5a0&t=4379

Ejemplo de uso de la shell de Flask para insertar y ver datos de la DB:

flask --app todo_app shell
Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] on linux
App: todo_app
Instance: /home/enrique/Development/Python/flask-todo-list/instance
>>> from todo_app.models import User, Todo
>>> from todo_app import db
# Para users
>>> user = User('emarifer', '123456')
>>> users = User.query.all()
>>> users
[]
>>> db.session.add(user)
>>> db.session.commit()
>>> users = User.query.all()
>>> users
[<User: emarifer>]
# Para todos
>>> todo1 = Todo(1, 'Aprendiendo Flask', 'descripción')
>>> todo2 = Todo(1, 'Reaprendiendo Python', 'descripción')
>>> db.session.add(todo1)
>>> db.session.add(todo2)
>>> db.session.commit()
>>> todos = Todo.query.all()
>>> todos
[<Todo: Aprendiendo Flask>, <Todo: Reaprendiendo Python>]
>>>

VARIABLES EN JINJA2:
https://stackoverflow.com/questions/3727045/set-variable-in-jinja

**kwargs. VER:
https://www.freecodecamp.org/news/args-and-kwargs-in-python/#:~:text=**kwargs%20allows%20us%20to,denote%20this%20type%20of%20argument.

OBJETO "g" EN FLASK Y APP CONTEXT. VER:
https://stackoverflow.com/questions/30514749/what-is-the-g-object-in-this-flask-code
https://flask.palletsprojects.com/en/3.0.x/api/#flask.g
https://flask.palletsprojects.com/en/3.0.x/appcontext/

FUNCIÓN "get_or_404". VER:
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#flask_sqlalchemy.SQLAlchemy.get_or_404

ORDER_BY DESC EN SQLALCHEMY. VER:
https://medium.com/@jesscsommer/survival-guide-for-flask-sqlalchemy-queries-e442bbaf9ad

How To Structure a Large Flask Application with Flask Blueprints and Flask-SQLAlchemy. VER:
https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

Best Folder and Directory Structure for a Flask Project. VER:
https://studygyaan.com/flask/best-folder-and-directory-structure-for-a-flask-project

Common folder/file structure in Flask app. VER:
https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app

Convenciones de nombres de archivos y otros en Python. VER:
https://www.delftstack.com/es/howto/python/file-naming-conventions-in-python/#convenci%c3%b3n-de-nomenclatura-para-archivos-en-python

"""