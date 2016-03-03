from datetime import datetime
from flask import render_template,session,redirect,url_for,flash
from flask.ext.login import login_required
from . import main


from ..libbase.dawxform  import KaiquForm

@main.route('/', methods=['GET', 'POST'])
@main.route('/index.html', methods=['GET', 'POST'])
@login_required
def index():
    
    return render_template('index.html' )
