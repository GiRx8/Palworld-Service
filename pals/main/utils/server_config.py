from flask import Blueprint, current_app, render_template, request, url_for, redirect
import re
from main.configurations.config import Config
from main.auth import admin_required
from main.db import get_db

bp = Blueprint('ini', __name__)

def parse_option_settings(data):
    start_index = data.find('OptionSettings=(') + len('OptionSettings=(')
    end_index = data.find(')', start_index)
    
    if start_index != -1 and end_index != -1:
        return data[start_index:end_index]
    else:
        return ''

def parse_option_values(values):
    return dict(pair.split('=', 1) for pair in values.split(',') if '=' in pair)

###Rewrite this file path loading method to be used across other utilities#####
def load_paths_from_db():
    db = get_db()
    config_row = db.execute('SELECT * FROM configs WHERE name = ?', ('PalWorldSettings',)).fetchone()
    
    return config_row

@bp.route('/config/ini')
@admin_required
def index():
    config_data = load_paths_from_db()
    
    if config_data:
        ini_file_path = config_data['path']
        with open(ini_file_path, 'r') as file:
            data = file.read()

        option_settings = parse_option_settings(data)
        option_values = parse_option_values(option_settings)

        return render_template('parsing/index.html', option_values=option_values)

@bp.route('/update', methods=['POST'])
@admin_required
def update():
    if request.method == 'POST':
        config_data = load_paths_from_db()

        if config_data:
            ini_file_path = config_data['path']  # Access 'path' attribute from the database result
            with open(ini_file_path, 'r') as file:
                data = file.read()

            option_settings = parse_option_settings(data)
            option_values = parse_option_values(option_settings)

            for key, value in request.form.items():
                if '"' in value and not (value.startswith('"') and value.endswith('"')):
                    option_values[key] = f'"{value}"'
                else:
                    option_values[key] = value

            new_option_settings = f'OptionSettings=({",".join([f"{key}={value}" for key, value in option_values.items()])})'

            data = re.sub(r'OptionSettings=\(.*\)', new_option_settings, data)

            with open(ini_file_path, 'w') as file:
                file.write(data)

    return redirect(url_for('ini.index'))