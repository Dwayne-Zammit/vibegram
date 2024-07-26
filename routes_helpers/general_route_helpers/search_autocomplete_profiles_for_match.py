import sqlite3
from helpers.user_helpers import get_profile_picture

def search_autocomplete_profiles_for_match_helper(filter):
    limit = 10
    connection = sqlite3.connect("instance/login.db")
    cursor = connection.cursor()
    query = f"select username from user where username like '%{filter}%'"
    cursor.execute(query)
    rows = cursor.fetchmany(limit)
    users = [user[0] for user in rows]
    users_results = {}
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    for user in users:
        users_results[user] = "static/profile_pictures/" + get_profile_picture(cursor, user)
    return users_results