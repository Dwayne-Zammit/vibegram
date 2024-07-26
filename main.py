import os, sys
from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from models import db, User

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from routes.direct_messages_routes import direct_messages_routes, socketio_bp
from routes.login_related_routes import login_related_routes
from routes.vibegram_relates_routes import vibegram_related_routes

# initialize the app
global app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['UPLOAD_FOLDER'] = 'static/profile_pictures'
app.config['STORIES_FOLDER'] = 'static/stories'
app.config['POSTS'] = 'static/posts'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

socketio = SocketIO(app, cors_allowed_origins='*')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_related_routes.login'

# create all tables
@app.before_first_request
def create_tables():
    db.create_all()

# load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# initialize login routes
app.register_blueprint(login_related_routes)

# initialize direct messages routes
app.register_blueprint(direct_messages_routes)

# vibegram related routes
app.register_blueprint(vibegram_related_routes)

# socket routes
socketio_bp(socketio)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)