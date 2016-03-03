from flask import Blueprint

dawxinfo = Blueprint('dawxinfo',__name__,url_prefix='/dawxinfo')

from . import views
