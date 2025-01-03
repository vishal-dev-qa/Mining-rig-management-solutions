from flask import Blueprint, render_template, request
from src.api.handlers import example_handler

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/')
def index():
    return render_template('index.html')

@api_blueprint.route('/dashboard', methods=['POST'])
def dashboard():
    ip_address = request.form.get(ip_address, '')
    print(ip_address)
    return render_template('dashboard.html', ip_address=ip_address)