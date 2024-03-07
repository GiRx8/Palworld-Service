from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
import subprocess
from main.auth import admin_required
from main.db import get_db
from main.__init__ import create_app
import psutil
import threading
import time


service_control_bp = Blueprint('service_control', __name__)

def get_service_status():
    try:
        status_command = '/usr/bin/sudo /bin/systemctl is-active palworld.service'
        result = subprocess.run(status_command, shell=True, capture_output=True, text=True)

        return result.stdout.strip().lower()
    except Exception as e:
        return f"Error getting service status: {e}"
    
def load_paths_from_db():
    db = get_db()
    config_row = db.execute('SELECT * FROM configs WHERE name = ?', ('PalWorldSettings',)).fetchone()
    
    return config_row
from flask import redirect, url_for, current_app

def perform_service_action(action):
    try:
        command = f'/usr/bin/sudo /bin/systemctl {action} palworld.service'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout, 'success'
        else:
            return result.stderr, 'failure'
    except Exception as e:
        return str(e), 'failure'

@service_control_bp.route('/stop-service', methods=['POST'])
@admin_required
def stop_service():
    result, status = perform_service_action('stop')
    return redirect(url_for('main.home', result=result, status=status))

@service_control_bp.route('/start-service', methods=['POST'])
@admin_required
def start_service():
    result, status = perform_service_action('start')
    return redirect(url_for('main.home', result=result, status=status))

@service_control_bp.route('/restart-service', methods=['POST'])
@admin_required
def restart_service():
    result, status = perform_service_action('restart')
    return redirect(url_for('main.home', result=result, status=status))

def get_system_info():
    # Get system information
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return {
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'disk_usage': disk_usage
    }

def emit_system_info():
    while True:
        # Sleep for a short interval (e.g., 1 second)
        time.sleep(1)

        # Emit the data to the connected clients
        create_app.config['system_info'] = get_system_info()

@service_control_bp.route('/test')
def index():
    return render_template('services/index_simple.html')

@service_control_bp.route('/get-system-info')
def get_system_info_route():
    return jsonify(get_system_info())

"""
@service_control_bp.route('/services/control-panel')
@admin_required
def control_panel():
    service_status = get_service_status()
    result = request.args.get('result')
    error = request.args.get('error')
    return render_template('services/control_panel.html', service_status=service_status, result=result, error=error)
"""
"""
@service_control_bp.route('/services/control-panel')
@admin_required
def control_panel():

    service_status = get_service_status()
    result = request.args.get('result')
    error = request.args.get('error')

    #flash(result, 'success')
    flash(error, 'error')


    #return redirect(url_for('main.home', service_status=service_status, result=result))
    return render_template('home/dashboard.html', service_status=service_status, result=result)
"""