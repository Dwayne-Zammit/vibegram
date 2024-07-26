import sqlite3, os, sys

from flask import render_template, redirect, url_for, request
from flask_login import current_user

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from helpers.general_helpers import check_if_user_exists
from helpers.user_helpers import get_profile_picture, check_if_logged_in_user_already_following_user, get_posts_by_user, get_count_of_posts_by_user, get_count_of_users_followers, get_count_of_users_that_user_is_following, get_users_bio, get_information_of_users_following_user, get_information_of_users_that_user_is_following

def search_profile_route_helper():    
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()

    if request.method == "GET":
        username=request.args.get('profile_username')
    if request.method == "POST":
        username = request.form.get('search_username')
    # check if user does not exist
    if check_if_user_exists(username) == False:
        return render_template('home.html', user_does_not_exist=True, user=username)

    # check if user is searching own user
    if username == current_user.username:
        return redirect(url_for('vibegram_related_routes.profile'))

    image = get_profile_picture(cursor, username)
    image = r"static\profile_pictures" + "\\" + image
    
    # check if already following
    follow_button = check_if_logged_in_user_already_following_user(cursor, username)

    # get count of posts by user
    posts = get_count_of_posts_by_user(cursor, username)

    # get users posts
    posts_images = get_posts_by_user(cursor, username)

    # total followers for the searched profile
    followers = get_count_of_users_followers(cursor, username)
    
    # total users for the searched profile
    following = get_count_of_users_that_user_is_following(cursor, username)
    
    followers_information = get_information_of_users_following_user(cursor, username)

    following_information = get_information_of_users_that_user_is_following(cursor, username)

    ## get bio for searched user
    bio = get_users_bio(cursor, username)


    return render_template('search_profile.html', username=username, image=image, posts_images=posts_images, follow_button=follow_button, following=following, followers=followers, posts=posts, bio=bio, followers_information=followers_information, following_information=following_information)
