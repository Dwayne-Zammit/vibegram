import sqlite3
from flask import redirect, url_for
from flask_login import current_user

def add_comment_route_helper(comment):
    username = current_user.username
    comment = comment.replace("comment=","").split("`")
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    cursor.execute(f'insert into comments (username,image_name, comment_by, comment) \
    VALUES ( "{comment[0]}", "{comment[1]}", "{username}","{comment[2]}")')
    conn.commit()
    return redirect(url_for('vibegram_related_routes.view_photo', username_image_name=f"{comment[0]},{comment[1]}"))      