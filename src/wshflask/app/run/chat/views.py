#coding=utf-8
from flask import render_template,session,redirect,url_for,flash
from flask.ext.login import login_required
from flask.ext.socketio import emit,join_room,leave_room
import time
from . import chat
from ... import socketio



@socketio.on('joined',namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print message
    emit('status', {'servername': '实时后端数据传送：：：z( U__U )z (>＿<)}} (¯(∞)¯)','level':'(¯^¯ ) ','data':'(*^﹏^*)'})





@socketio.on('text', namespace='/chat')
def left(me):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    for i  in range(10):
        emit('message', {'msg':  me['msg']})



@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    emit('status', {'msg':  ' has left the room.'})

