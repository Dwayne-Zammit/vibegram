import sqlite3
from flask import current_app


def move_key_to_front(dct, key):
    if key not in dct:
        return dct

    new_dct = {key: dct[key]}
    for k, v in dct.items():
        if k != key:
            new_dct[k] = v
    return new_dct


# Create a function to check if the uploaded file has a valid extension
def allowed_file(filename, app=current_app):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def check_if_user_exists(username):
    conn = sqlite3.connect(r'./instance/login.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * from user where username = '{username}'")
        user_exists = cursor.fetchall()
        if len(user_exists) == 0:
            return False
        else:
            return True
    except:
        return False