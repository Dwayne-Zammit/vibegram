from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash
from flask_login import login_user

def login_route_post(password, user):
    if user and check_password_hash(user.password, password):
        login_user(user)
        flash('Login successful.', category='success')
        return redirect(url_for('vibegram_related_routes.home'))
    else:
        flash('Invalid username or password', category='error')
        return redirect(url_for('login_related_routes.login'))
    
def register_route_post(username, password, User, db):
    if not username or not password:
        flash('Both username and password are required.', category='error')
        return render_template('register.html')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists. Please choose a different one.', category='error')
        return render_template('register.html')
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful. Please log in.', category='success')
    return redirect(url_for('login_related_routes.login'))