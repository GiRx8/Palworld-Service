from flask import Blueprint, render_template, g, flash, request
from main.auth import login_required, admin_required
from main.utils.service_control import get_service_status
from main.db import get_db

Configs_bp = Blueprint('Configs', __name__)

bp = Blueprint('main', __name__)

@bp.route('/')
@admin_required
def home():
    g.db = get_db()
    cursor_path = g.db.execute("SELECT name, path FROM configs")
    results_path = cursor_path.fetchall()

    cursor_user = g.db.execute("SELECT id, username, is_admin FROM user")
    results_user = cursor_user.fetchall()

    cursor_path.close()
    cursor_user.close()

    service_status = get_service_status()
    result = request.args.get('result')
    error = request.args.get('error')

    #flash(result, 'success')
    #flash(error, 'error')

    return render_template('home/dashboard.html', results_path=results_path, results_user=results_user, service_status=service_status, result=result)

@bp.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')
