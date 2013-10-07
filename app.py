"""
    GitHub Example
    --------------

    Shows how to authorize users with Github.

"""
from flask import Flask, request, g, session, redirect, url_for
from flask import render_template_string
from flask.ext.github import *

# Set these values
GITHUB_CLIENT_ID = 'fc3ea1198ec2a0ecd673'
GITHUB_CLIENT_SECRET = 'ab47a318577cd95bec78686555f0ceaf8b9a80f5'
GITHUB_CALLBACK_URL = 'http://alphabet.io'

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)

# setup github-flask
github = GitHub(app)

def init_db():
    Base.metadata.create_all(bind=engine)

class User(Document):
    def __init__(self, name, github_access_token):
        self.name = name
        self.github_access_token = github_access_token

class Project(Document):
    def __init__(self, name, url, user):
        self.name = name
        self.url = url
        self.user = user

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response


@app.route('/')
def index():
    if g.user:
        t = 'Hello! <a href="{{ url_for("user") }}">Get user</a> ' \
            '<a href="{{ url_for("logout") }}">Logout</a>'
    else:
        t = 'Hello! <a href="{{ url_for("login") }}">Login</a>'

    return render_template_string(t)


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)
    user.github_access_token = access_token
    db_session.commit()

    session['user_id'] = user.id
    return redirect(url_for('index'))


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/user')
def user():
    return str(github.get('user'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

