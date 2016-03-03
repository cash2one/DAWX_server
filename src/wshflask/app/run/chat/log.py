from datetime import datetime
from flask import render_template,session,redirect,url_for,flash,request
from flask.ext.login import login_required
from flask.ext.socketio import emit,join_room,leave_room
from . import chat

from ... import socketio
from ...webclient import runcmd



@chat.route('/index.html')
@chat.route('/')
def index():
    return render_template('chat/index.html')

@chat.route('/getlog.html',methods=['POST'])
def getlog():
    if request.method == 'POST':
        socketio.emit('status', {'servername': str(request.form['servername']), 'level': str(request.form['level']) ,'data': str(request.form['data']) },namespace='/chat')
        return "OK"
    else:
        return "WRONG"

@chat.route('/message.html',methods=['GET'])
def message():
    return render_template('chat/message.html')


