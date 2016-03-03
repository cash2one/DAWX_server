#coding=utf-8

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO
from config import config
import os


bootstrap = Bootstrap()
login_manager = LoginManager()
db = SQLAlchemy()
socketio = SocketIO()

login_manager.session_protection ='strong'
login_manager.login_view = 'auth.login'
# 不知道怎么搞这个全局变量，只好这么做了，感觉不太好
globalconfig = config['development']()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    #bootstrap_find_resource(local=True);
    #app.config.setdefault('BOOTSTRAP_SERVER_LOCAL',True)
    login_manager.init_app(app)
    db.init_app(app)
    socketio.init_app(app)

    # 附带的路由以及自定义的错误页面
    from .run.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .run.dawx import dawx as dawx_blueprint
    app.register_blueprint(dawx_blueprint)
    from .run.about import about as about_blueprint
    app.register_blueprint(about_blueprint)
    from .run.sginfo import sginfo as sginfo_blueprint
    app.register_blueprint(sginfo_blueprint)
    from .run.api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    from .run.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .run.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    from .run.dawxinfo import dawxinfo as dawxinfo_blueprint
    app.register_blueprint(dawxinfo_blueprint)
    return app

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')


