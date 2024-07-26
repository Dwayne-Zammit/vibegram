import sqlite3
from flask import render_template, flash
from flask_login import  current_user

def view_photo_route_helper(username_image_name):
    username_image_name = username_image_name.replace("username_image_name=", "").split(",")
    print(username_image_name)
    print(len(username_image_name))
    username = username_image_name[0]
    image_name = username_image_name[1]
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT profile_pictures.username, profile_pictures.image_name as profile_picture, posts.image_name as post_image_name from posts inner \
    join profile_pictures on posts.username = profile_pictures.username where posts.username='{username}' and posts.image_name='{image_name}'")
    print(f"SELECT profile_pictures.username, profile_pictures.image_name as profile_picture, posts.image_name as post_image_name from posts inner \
    join profile_pictures on posts.username = profile_pictures.username where posts.username='{username}' and posts.image_name='{image_name}'")
    results = cursor.fetchall()
    if len(results) < 0:
        flash("nothing was found")         
    comments_query = f"select comments.username, comments.image_name, comments.comment_by, comments.comment, profile_pictures.image_name as comment_by_profile_picture \
    from comments INNER JOIN profile_pictures on profile_pictures.username = comments.comment_by where comments.username = '{username}' and comments.image_name = '{image_name}'"
    cursor.execute(comments_query)
    comments_results = cursor.fetchall()
    if len(comments_results) > 0:
        print(comments_results)
    if username == current_user.username:
        return render_template('edit_post.html', results=results, comments=comments_results)
    else:    
        return render_template('view_photos.html', results=results, comments=comments_results)