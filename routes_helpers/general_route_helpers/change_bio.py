import sqlite3
from flask_login import current_user
from flask import redirect, url_for

def change_bio_route_helper(bio):
    username = current_user.username
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM bio where username = '{username}'")
        conn.commit()
    except:
        print("no records")
    bio = str(bio).replace('"', "'")    
    cursor.execute(f'INSERT INTO profile_bio values ("{username}","{bio}")')
    conn.commit()
    return redirect(url_for('vibegram_related_routes.profile'))
    