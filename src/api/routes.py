from flask import Blueprint, render_template, request, jsonify
from src.api.handlers import call_cgminer
import requests

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/')
def index():
    return render_template('index.html')


@api_blueprint.route('/dashboard', methods=['POST'])
def dashboard():
    ip_address = request.form.get('ip_address', '')
    return render_template('dashboard.html', ip_address=ip_address)


@api_blueprint.route('/trigger', methods=['POST'])
def trigger():
    try:
        data = request.json
        ip = data.get('ip')
        command = data.get('command')

        if not ip or not command:
            return jsonify({"error": "IP and command are required."}), 400

        response = call_cgminer(ip, command)
        return jsonify(response)

    except requests.ConnectionError:
        return jsonify({"error": "Failed to connect to the specified IP and endpoint."}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500