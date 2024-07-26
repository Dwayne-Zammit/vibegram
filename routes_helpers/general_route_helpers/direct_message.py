import sqlite3
from flask_login import current_user
from flask import render_template


def direct_message_route_helper(user1_id):
    user2_id = current_user.username
    if current_user.username == user1_id or current_user.username == user2_id:
        room_id = sorted([user1_id, user2_id], key=str)
        room_id = f"{room_id[0]}-{room_id[1]}"
        print(current_user.username)
        print(user1_id)
        print(user2_id)
        #### get previous chat 
        conn = sqlite3.connect(r'./database/database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT sender, message, date, image_name as profile_picture FROM direct_messages\
        INNER JOIN profile_pictures ON profile_pictures.username = direct_messages.sender WHERE (sender = '{user1_id}' OR b_party = '{user1_id}') \
        AND (sender = '{user2_id}' OR b_party = '{user2_id}') ORDER BY date")
        print(f"SELECT sender, message, date, image_name as profile_picture FROM direct_messages\
        INNER JOIN profile_pictures ON profile_pictures.username = direct_messages.sender WHERE sender = '{user1_id}' OR b_party = '{user1_id}' \
        AND sender = '{user2_id}' OR b_party = '{user2_id}' ORDER BY date")
        results = cursor.fetchall()
        if len(results) > 0:
            for message in results:
                print(message)
        else:
            print("No existing messages")
        return render_template('direct_messages.html', room=room_id, previous_messages=results, username=current_user.username)
  
    else:     
        return("Unauthorized")         