import sqlite3, os
from datetime import datetime
from flask_login import current_user
from flask import redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from helpers.general_helpers import allowed_file
from flask import current_app


def add_story_route_helper(app=current_app):
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
        now = datetime.now()
        formatted_now = now.strftime("%d/%m/%y %H:%M")
        cursor.execute(f"insert into stories values('{username}','{filename}', '{formatted_now}')")
        conn.commit()
        file.save(os.path.join(app.config['STORIES_FOLDER'], filename))
        return redirect(url_for('vibegram_related_routes.home'))