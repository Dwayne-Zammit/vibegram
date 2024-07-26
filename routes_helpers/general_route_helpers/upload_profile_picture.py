import sqlite3, os
from flask import redirect, flash, request, url_for
from flask_login import current_user
from helpers.general_helpers import allowed_file
from werkzeug.utils import secure_filename
from flask import current_app


def upload_profile_picture_route_helper(app=current_app):
    username = current_user.username
    if 'image' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        flash('Image uploaded successfully', category='success')
        conn = sqlite3.connect(r'./database/database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM profile_pictures where username = '{username}'")
            conn.commit()
        except:
            print("issue with deleting")

        cursor.execute(f"insert into profile_pictures values('{username}','{filename}')")
        conn.commit()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('vibegram_related_routes.profile'))
    else:
        flash('Invalid file type', category='error')
        return redirect(request.url)