import sqlite3
from flask import redirect, url_for
from flask_login import current_user

def delete_photo_route_helper(username_image_name):
    username_image_name = username_image_name.replace("username_image_name=","").split(",")
    if username_image_name[0] == current_user.username:
        conn = sqlite3.connect(r'./database/database.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM POSTS WHERE username='{username_image_name[0]}' and image_name='{username_image_name[1]}'")
        conn.commit()
        cursor.execute(f"DELETE FROM comments WHERE username='{username_image_name[0]}' and image_name='{username_image_name[1]}'")
        conn.commit()
        return redirect(url_for('vibegram_related_routes.profile'))
    else:
        return("Not Authorized")  