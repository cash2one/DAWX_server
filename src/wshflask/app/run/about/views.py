from datetime import datetime
from flask import render_template,session,redirect,url_for

from . import about

@about.route('/')
@about.route('/dawx.html')
def dawx():
    return '<h1>DAWX</h1>'

@about.route('/product.html')
def product():
    return '<h1>PRODUCT</h1>'

@about.route('/me.html')
def me():
    return '<h1>ME</h1>'
     
