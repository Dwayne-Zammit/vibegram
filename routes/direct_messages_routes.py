import os
import sys
from flask import Blueprint
from flask_login import login_required
from flask_socketio import join_room, leave_room
from routes_helpers.general_route_helpers.direct_message import direct_message_route_helper
from routes_helpers.general_route_helpers.handle_messages_sent import handle_messages_sent_route_helper

direct_messages_routes = Blueprint('direct_messages', __name__)

# Direct message route
@direct_messages_routes.route('/directMessage/<user1_id>')
@login_required
def directMessage(user1_id):
    return direct_message_route_helper(user1_id)

def socketio_bp(socketio):
    # Handle messages sent
    @socketio.on('message')
    def handle_message(message, room, sender):
        return handle_messages_sent_route_helper(message, room, sender)

    @socketio.on('join')
    def on_join(room):
        join_room(room)

    @socketio.on('leave')
    def on_leave(room):
        leave_room(room)
