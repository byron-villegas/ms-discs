from flask import Blueprint

bp = Blueprint("discs", __name__)

from app.discs import routes