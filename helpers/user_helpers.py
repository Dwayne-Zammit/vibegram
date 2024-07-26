from datetime import datetime, timedelta
import random
import json
from flask_login import current_user
import sqlite3

def get_profile_picture(cursor , username):
    cursor.execute(f"SELECT image_name FROM profile_pictures WHERE username = '{username}'")
    profile_picture = cursor.fetchall()
    if len(profile_picture) > 0:
        for line in profile_picture:
            profile_picture = line[0]
    else:
        profile_picture = "default-no-profile-pic.jpg"        
    return profile_picture
    

def get_stories(cursor, current_user):
    now = datetime.now()    
    one_day_ago = now - timedelta(days=1)
    formatted_one_day_ago = one_day_ago.strftime("%d/%m/%y %H:%M")
    print(formatted_one_day_ago)
    ### check if user posted in the last 24 hours ###
    cursor.execute(f'select following.is_following, MAX(stories.image_name) as storie_image_name, MAX(profile_pictures.image_name) as profile_picture \
    from stories inner join following on following.is_following = stories.username inner join profile_pictures on profile_pictures.username = \
    stories.username where following.username = "{current_user.username}" and stories.date > "{formatted_one_day_ago}" group by following.is_following order by date DESC')
    results = cursor.fetchall()
    stories = []
    if len(results) > 0:
        for storie in results:
            if storie[0] != current_user.username:
                stories.append(storie)   
    return stories

def get_logged_in_user_posts(cursor, current_user):
    username = current_user.username
    # try to get posts
    cursor.execute(f"SELECT image_name from posts where username = '{username}'")
    results = cursor.fetchall()
    cursor.execute(f"SELECT count(image_name) from posts where username = '{username}'")
    posts = cursor.fetchall()
    if len(posts) != 0:
        for post in posts:
            posts = post[0]
        if int(posts) == 1:
            posts = str(posts)
            posts += " Post"
        else:
            posts = str(posts)
            posts += " Posts"
    else:
        posts = 0  
    posts_images = []
    # post_images_html = []
    if len(results) != 0:
        for result in results:
            for image_name in result:
                posts_images.append(image_name)
    return posts, posts_images

def get_posts_user_is_following(cursor, current_user):
    cursor.execute(f"select posts.username, posts.image_name, profile_pictures.image_name as profile_picture from following \
    inner join posts on posts.username = is_following inner join profile_pictures on profile_pictures.username = following.is_following where following.username = '{current_user.username}'")
    results = cursor.fetchall()
    posts_images = []
    if len(results) != 0:
        for line in results:
            posts_images.append(line)
    random.shuffle(posts_images)   
    return posts_images 



def get_count_of_users_followers(cursor, username):
    cursor.execute(f"SELECT count(*) from following where is_following = '{username}'")
    followers = cursor.fetchall()
    if len(followers) != 0:
        for line in followers:
            followers=line[0]
        if int(followers) == 1:
            followers = str(followers)
            followers += " Follower"
        else:
            followers = str(followers)
            followers += " Followers"     
    else:
        followers="0 followers"
    return followers        



def get_information_of_users_following_user(cursor, username):
    cursor.execute(f"SELECT following.username, image_name as 'profile_picture' from following inner join profile_pictures on following.username = profile_pictures.username where is_following = '{username}'")
    followers_information = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    # Convert the fetched data to a list of dictionaries
    followers_list = []
    for row in followers_information:
        row_dict = dict(zip(columns, row))
        followers_list.append(row_dict)

    # Convert the list of dictionaries to a JSON string
    followers_info_json = json.dumps(followers_list)
    return json.loads(followers_info_json)


def get_count_of_users_that_user_is_following(cursor, username):
    ## check_following_count
    cursor.execute(f"SELECT count(*) from following where username = '{username}'")
    following = cursor.fetchall()
    if len(following) != 0:
        for line in following:
            following=line[0]
        following = str(following)    
        following += " Following"     
    else:
        following = str(following)
        following="0 following"
    return following

def get_information_of_users_that_user_is_following(cursor, username):
    cursor.execute(f"SELECT following.is_following, image_name as 'profile_picture' from following inner join profile_pictures on following.is_following = profile_pictures.username where following.username = '{username}'")
    followers_information = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    # Convert the fetched data to a list of dictionaries
    following_list = []
    for row in followers_information:
        row_dict = dict(zip(columns, row))
        following_list.append(row_dict)

    # Convert the list of dictionaries to a JSON string
    following_info_json = json.dumps(following_list)
    return json.loads(following_info_json)

def get_users_bio(cursor, username):
    cursor.execute(f"SELECT bio from profile_bio where username = '{username}'")
    bio = cursor.fetchall()
    if len(bio) > 0:
        for line in bio:
            bio = line[0]
    else:
        bio = "Hi, I'm a VibeGram user! Welcome to my profile."
    return bio

def check_if_logged_in_user_already_following_user(cursor, username):
    cursor.execute(f"SELECT * from following where username = '{current_user.username}' and is_following = '{username}'")
    is_following = cursor.fetchall()
    if len(is_following) != 0:
        follow_button = "False"
    else:
        follow_button = "True"
    return follow_button


def get_posts_by_user(cursor, username):
    cursor.execute(f"SELECT image_name from posts where username = '{username}'")
    posts_images_filenames = cursor.fetchall()
    posts_images = []
    if len(posts_images_filenames) != 0:
        for result in posts_images_filenames:
            for image_name in result:
                posts_images.append(image_name)
    return posts_images


def get_count_of_posts_by_user(cursor, username):
    cursor.execute(f"SELECT count(*) from posts where username = '{username}'")
    posts = cursor.fetchall()
    if len(posts) != 0:
        for line in posts:
            posts=line[0]
        if int(posts) == 1:
            posts = str(posts)
            posts += " Post"
        else:
            posts = str(posts)
            posts += " Posts"   
    else:
        posts="0 posts"
    return posts    
