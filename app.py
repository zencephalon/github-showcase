"""
    GitHub Example
    --------------

    Shows how to authorize users with Github.

"""
from flask import Flask, request, g, session, redirect, url_for
from flask import render_template_string
from flask import *
from flask.ext.github import *
import pdb

# Set these values
GITHUB_CLIENT_ID = 'fc3ea1198ec2a0ecd673'
GITHUB_CLIENT_SECRET = 'ab47a318577cd95bec78686555f0ceaf8b9a80f5'
GITHUB_CALLBACK_URL = 'http://alphabet.io/github-callback'

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
        SECRET_KEY='ASECRETSOTERRIBLE'
        )

# setup github-flask
github = GitHub(app)

class User():
    def __init__(self, github_access_token):
        self.github_access_token = github_access_token
        self.id = 100 # change this

class Project():
    def __init__(self, name, url, user):
        self.name = name
        self.url = url
        self.user = user

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = "matt" # change this too


@app.after_request
def after_request(response):
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

    user = User(access_token)

    session['user_id'] = "hello"
    #pdb.set_trace()
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

@app.route('/project')
def project():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True,port=4000,host='0.0.0.0')

