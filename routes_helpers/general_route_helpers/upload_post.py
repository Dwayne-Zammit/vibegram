import sqlite3, os
from flask_login import current_user
from flask import redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from helpers.general_helpers import allowed_file
from flask import current_app


def upload_post_route_helper():
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
        cursor.execute(f"insert into posts values('{username}','{filename}')")
        conn.commit()
        file.save(os.path.join(current_app.config['POSTS'], filename))
        return redirect(url_for('vibegram_related_routes.profile'))
    else:
        flash('Invalid file type', category='error')
        return redirect(request.url)
