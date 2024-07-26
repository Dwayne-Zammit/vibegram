import sqlite3, sys, os
from flask import render_template
from flask_login import current_user


current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from helpers.user_helpers import get_profile_picture, get_logged_in_user_posts, get_count_of_users_followers, get_count_of_users_that_user_is_following, get_users_bio, get_information_of_users_following_user, get_information_of_users_that_user_is_following

def get_logged_in_user_profile():
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    username = current_user.username

    # get profile picture
    image_path = get_profile_picture(cursor, current_user.username)
    image = r"static\profile_pictures" + "\\" + image_path
    # try to get posts
    posts, posts_images = get_logged_in_user_posts(cursor, current_user)
    ## check_followers_count
    followers = get_count_of_users_followers(cursor, username)
    ## check_following_count
    following = get_count_of_users_that_user_is_following(cursor, username)
    # get users bio 
    bio = get_users_bio(cursor, username)

    followers_information = get_information_of_users_following_user(cursor, username)

    following_information = get_information_of_users_that_user_is_following(cursor, username)
    return render_template('profile.html', username=username, image=image, posts_images=posts_images, user=username, posts=posts, followers=followers, following=following, bio=bio, followers_information=followers_information, following_information=following_information)

