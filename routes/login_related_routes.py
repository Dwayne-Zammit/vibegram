# login_routes.py
import os
import sys
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user
from models import User
from routes_helpers.general_route_helpers.authentication_routes import login_route_post, register_route_post
from models import db, User

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

login_related_routes = Blueprint('login_related_routes', __name__)

# login route
@login_related_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        return login_route_post(password, user)

# register route  
@login_related_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return register_route_post(username, password, User, db)

# logout route
@login_related_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', category='success')
    return redirect(url_for('login_related_routes.login'))
