from flask import Blueprint

main = Blueprint('main', __name__)

from . import book_route, library_route, user_route 