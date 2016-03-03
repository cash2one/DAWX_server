from flask import Blueprint

about = Blueprint('about',__name__,url_prefix="/about")
from . import views

