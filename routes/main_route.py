from flask import jsonify, render_template
from routes.init import main
import http_status as status

@main.route('/')
def index():
    return jsonify("This is home page"), status.HTTP_OK

