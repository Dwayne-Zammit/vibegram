
import sqlite3
from flask_login import current_user
from flask import redirect, url_for


def unfollow_user_route_helper(profile_username):
    username = current_user.username
    # profile_username = request.args.get('profile_username')
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    cursor.execute(f"delete from following where username='{username}' and is_following='{profile_username}'")
    conn.commit()
    global user_to_show
    user_to_show = profile_username
    # return(f"You: {username} will follow {profile_username}")
    return redirect(url_for('vibegram_related_routes.home_search_bar_search_profile', profile_username=profile_username))