#!/usr/bin/env python
import os
from gevent import monkey
monkey.patch_all()

from app import create_app, db, socketio
#from app import app, db, socketio

from app.run.models import User,Role
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
    return dict(app=socketio, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
    #socketio.run(app,host="0.0.0.0")
