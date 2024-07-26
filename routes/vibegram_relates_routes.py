import os
import sys
from flask import Blueprint, request, redirect, url_for
from flask_login import login_required
from routes_helpers.general_route_helpers.home import home_route
from routes_helpers.general_route_helpers.users_profile import get_logged_in_user_profile
from routes_helpers.general_route_helpers.search_profile import search_profile_route_helper
from routes_helpers.general_route_helpers.view_stories import view_stories_route_helper
from routes_helpers.general_route_helpers.view_photo import view_photo_route_helper
from routes_helpers.general_route_helpers.edit_photo import edit_photo_route_helper
from routes_helpers.general_route_helpers.delete_photo import delete_photo_route_helper
from routes_helpers.general_route_helpers.add_comment import add_comment_route_helper
from routes_helpers.general_route_helpers.follow_user import follow_user_route_helper
from routes_helpers.general_route_helpers.unfollow_user import unfollow_user_route_helper
from routes_helpers.general_route_helpers.change_bio import change_bio_route_helper
from routes_helpers.general_route_helpers.upload_profile_picture import upload_profile_picture_route_helper
from routes_helpers.general_route_helpers.add_story import add_story_route_helper
from routes_helpers.general_route_helpers.upload_post import upload_post_route_helper
from routes_helpers.general_route_helpers.search_autocomplete_profiles_for_match import search_autocomplete_profiles_for_match_helper

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

vibegram_related_routes = Blueprint('vibegram_related_routes', __name__)

# index route
@vibegram_related_routes.route('/', methods=['GET', 'POST'])
def redir():
    if request.method == 'GET':
        return redirect(url_for('vibegram_related_routes.home'))

# home route
@vibegram_related_routes.route('/home')
@login_required
def home():
    return home_route()

# logged in user profile page
@vibegram_related_routes.route('/profile')
@login_required
def profile():
    return(get_logged_in_user_profile())

@vibegram_related_routes.route('/search_profile', methods=['GET', 'POST'])
@login_required
def home_search_bar_search_profile():
    return search_profile_route_helper()

# view stories
@vibegram_related_routes.route('/view_stories/<string:start_with>', methods=['GET', 'POST'])
@login_required
def view_stories_route(start_with):
    return view_stories_route_helper(start_with)

# view photo
@vibegram_related_routes.route('/view_photo/<string:username_image_name>', methods=['GET', 'POST'])
@login_required
def view_photo(username_image_name):
    if request.method == 'GET' or request.method == "POST":
        return view_photo_route_helper(username_image_name)

### view photo
@vibegram_related_routes.route('/edit_post/<string:username_image_name>', methods=['GET', 'POST'])
@login_required
def edit_post(username_image_name):
    if request.method == 'GET' or request.method == "POST":
        return edit_photo_route_helper(username_image_name)

### delete post
@vibegram_related_routes.route('/delete_post/<string:username_image_name>', methods=['GET', 'POST'])
@login_required
def delete_post(username_image_name):
    if request.method == "GET" or request.method == "POST":
        return delete_photo_route_helper(username_image_name)

### add comment
@vibegram_related_routes.route('/add_comment/<string:comment>', methods=['GET', 'POST'])
@login_required
def add_comment(comment):
    if request.method == "GET" or request.method == "POST":
        return add_comment_route_helper(comment)

### follow user
@vibegram_related_routes.route('/follow_user/<string:profile_username>', methods=['GET', 'POST'])
@login_required
def follow_user(profile_username):
    if request.method == "POST":
        return follow_user_route_helper(profile_username)

### unfollow user
@vibegram_related_routes.route('/unfollow_user/<string:profile_username>', methods=['GET', 'POST'])
@login_required
def unfollow_user(profile_username):
    if request.method == "POST":
        return unfollow_user_route_helper(profile_username)

### change bio
@vibegram_related_routes.route('/change_bio/<string:bio>', methods=['GET', 'POST'])
@login_required
def change_bio(bio):
    if request.method == "POST" or request.method == "GET":
        return change_bio_route_helper(bio)

# Add a new route to handle the image upload profile picture
@vibegram_related_routes.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    return upload_profile_picture_route_helper()

# Add a new story route
@vibegram_related_routes.route('/add-story', methods=['POST'])
@login_required
def add_story():
    return add_story_route_helper()

# Add a new post route
@vibegram_related_routes.route('/upload-post', methods=['POST'])
@login_required
def upload_post():
    return upload_post_route_helper()

# Add a new post route
@vibegram_related_routes.route('/autoCompleteUsersSearch/<string:filter>', methods=['GET'])
@login_required
def autoCompleteUsersSearch(filter):
    return search_autocomplete_profiles_for_match_helper(filter)