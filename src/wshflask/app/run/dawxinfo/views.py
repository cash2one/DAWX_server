#coding=utf-8
from flask import render_template,session,redirect,url_for,flash
from flask.ext.login import login_required
from flask.ext.socketio import emit,join_room,leave_room

import time
from . import dawxinfo

@dawxinfo.route('/')
@dawxinfo.route('/index.html')
def index():
    return render_template('dawxinfo/index.html')

@dawxinfo.route('/allusernum.html')
def allusernum():
    return render_template('dawxinfo/allusernum.html')


@dawxinfo.route('/oneusernum.html')
def oneusernum():
    return render_template('/dawxinfo/oneusernum.html')


@dawxinfo.route('/oneusernum_item.html')
def oneusernum_item():
    return render_template('/dawxinfo/oneusernum_item.html')


@dawxinfo.route('/valuenum.html')
def valuenum():
    return render_template('dawxinfo/valuenum.html')


@dawxinfo.route('/valuenum_item.html')
def valuenum_item():
    return render_template('dawxinfo/valuenum_item.html')

