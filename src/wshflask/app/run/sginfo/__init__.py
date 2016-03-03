from flask import Blueprint

sginfo = Blueprint('sginfo',__name__,url_prefix='/sginfo')
from . import views



