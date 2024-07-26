import sqlite3
from flask_login import current_user
from flask_socketio import emit
from datetime import datetime

def handle_messages_sent_route_helper(message, room, sender):
    ## get_profile_picture
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT image_name from profile_pictures where username='{current_user.username}'")
    result = cursor.fetchall()
    image_name = ("default-no-profile-pic.jpg")
    if len(result) >= 0:
        for line in result:
            image_name = line[0]
        print(image_name)  
    #### get date and time ####
    now = datetime.now() 
    now = now.strftime("%d/%m/%y %H:%M")
    #####
    ##### insert message into database
    usernames = room.split("-")
    if usernames[0] == current_user.username:
        b_party = usernames[1]
    elif usernames[1] == current_user.username:   
        b_party = usernames[0]
    query = f'INSERT INTO direct_messages (sender, b_party, message, date)\
    VALUES("{current_user.username}", "{b_party}", "{message}", "{now}")'
    conn = sqlite3.connect(r'./database/database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print(room)
    print(f'Room {room}: {sender}: {message}')
    emit('message', {'text': message, 'sender': current_user.username, 'profile_picture': image_name, 'datetime': now}, room=room) 
    return
