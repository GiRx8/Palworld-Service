import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from main.auth import admin_required
from main.db import get_db

Configs_bp = Blueprint('Configs', __name__)


class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    INSTANCE_PATH=os.path.join(BASE_DIR, 'instance')
    DATABASE=os.path.join(BASE_DIR, INSTANCE_PATH, 'flaskr.sqlite')
    SCRIPT_FILE_PATH = os.path.join('/home/steam/Steam/steamapps/common/PalServer')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    ####Fix data implementation of path####
    #INI_FILE_PATH = os.path.join(BASE_DIR, '../PalWorldSettings.ini')
    #INI_FILE_PATH = os.path.join('/home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini')

@Configs_bp.route('/update_path/<name>', methods=['GET', 'POST'])
@admin_required
def update_path(name):
    db = get_db()

    existing_config = db.execute('SELECT * FROM configs WHERE name = ?', (name,)).fetchone()

    if existing_config is None:
        flash(f'Configuration with name {name} not found', 'error')
        return redirect(url_for('main.home'))  # Redirect to another page or handle appropriately

    if request.method == 'POST':
        new_path = request.form.get('new_path')

        if not new_path:
            flash('Missing new_path parameter', 'error')
            return redirect(url_for('Configs.update_path', name=name))

        db.execute('UPDATE configs SET path = ? WHERE name = ?', (new_path, name))
        db.commit()

        flash(f'Path for configuration {name} updated successfully', 'success')

        return redirect('/')

    return render_template('misc/update_path.html', config_name=name)
