from flask import render_template
from flask_login import current_user
import sqlite3
import os, sys

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from helpers.user_helpers import get_stories, get_profile_picture, get_posts_user_is_following

def home_route():
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()

    #  get posts for users that user is following
    posts_images = get_posts_user_is_following(cursor, current_user)

    # get profile_picture filename
    profile_picture = get_profile_picture(cursor, current_user.username)

    # get stories
    stories = get_stories(cursor, current_user)
    return render_template('home.html', user_does_not_exist=False, posts_images=posts_images, profile_picture=profile_picture, stories=stories)