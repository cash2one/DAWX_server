from datetime import datetime
from flask import render_template,session,redirect,url_for
from flask.ext.login import login_required

from . import sginfo

from ..libbase.add_item import DawxZabbix
from ..libbase.dbnuminfo import getdbnuminfo
from ..libbase.serverinfo import getserverinfo

@sginfo.route('/')
@sginfo.route('/index.html')
@login_required
def index():
    return render_template('sginfo/index.html')



@sginfo.route('/dbnuminfo.html')
@login_required
def dbnuminfo():
    alist = getdbnuminfo()
    return render_template('sginfo/dbnuminfo.html',alist=alist)


@sginfo.route('/serverinfo.html')
@login_required
def serverinfo():
    alist = getserverinfo()
    return render_template('sginfo/serverinfo.html',alist = alist)



@sginfo.route('/cpuinfo.html')
@login_required
def cpuinfo():
    #ainstance = DawxZabbix()
    #hostsjson = ainstance.getcommonhosts()
    return render_template('sginfo/cpuinfo.html')

@sginfo.route('/product.html')
@login_required
def product():
    return '<h1>PRODUCT</h1>'

@sginfo.route('/me.html')
@login_required
def me():
    return '<h1>ME</h1>'

