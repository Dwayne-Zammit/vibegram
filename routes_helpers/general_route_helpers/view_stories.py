import sqlite3, os, sys

from flask import render_template, request
from flask_login import  current_user
from datetime import datetime, timedelta

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from helpers.general_helpers import move_key_to_front

def view_stories_route_helper(start_with):
    start_with = start_with.replace("start_with=","")
    images_per_user = {}
    if request.method == "GET":
        username = current_user.username
        now = datetime.now()    
        one_day_ago = now - timedelta(days=1)
        formatted_one_day_ago = one_day_ago.strftime("%d/%m/%y %H:%M")
        query_stories = f"SELECT following.is_following,stories.image_name as storie_image_name, stories.date, profile_pictures.image_name as profile_picture_image_name from following inner \
        join stories on following.is_following = stories.username inner join profile_pictures on stories.username = profile_pictures.username where following.username = '{username}' and date > '{formatted_one_day_ago}'"
        conn = sqlite3.connect(r'./database/database.db')
        cursor = conn.cursor()
        cursor.execute(query_stories)
        results = cursor.fetchall()
        for line in results:
            user_id = line[0]
            image_id = line[1]
            profile_picture = line[3]

             # if the user ID is already in the dictionary, add the new image ID to the existing list
            if user_id in images_per_user:
                images_per_user[user_id]['images'].append({'image_id': image_id})
            # otherwise, create a new list with the image ID as the first element
            else:
                images_per_user[user_id] = {'profile_picture': profile_picture, 'images': [{'image_id': image_id}]}
        images_per_user = move_key_to_front(images_per_user, start_with)
        # for key,value in images_per_user.items():
        #     print(key,value)
        return render_template('stories.html', images_per_user=images_per_user)