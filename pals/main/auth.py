import functools

from functools import wraps
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from main.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        g.user = get_user_by_id(session['user_id'])
        
        return view(*args, **kwargs)

    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None or not g.user.get('is_admin', False):
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
@admin_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form  # Check if the checkbox is checked
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), is_admin),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect('/')

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)

    return render_template('auth/login.html')

@bp.route('/reset-password', methods=('GET', 'POST'))
@login_required
def reset_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        db = get_db()
        error = None

        if not check_password_hash(g.user['password'], current_password):
            error = 'Invalid current password.'
        elif new_password != confirm_password:
            error = 'New password and confirm password do not match.'
        else:
            db.execute(
                "UPDATE user SET password = ? WHERE id = ?",
                (generate_password_hash(new_password), g.user['id']),
            )
            db.commit()

            flash('Password reset successfully.')
            return redirect('/')

        flash(error)

    return render_template('auth/reset_password.html')

@bp.route('/delete-user/<int:user_id>', methods=('GET', 'POST'))
@admin_required
def delete_user(user_id):
    db = get_db()
    error = None

    if request.method == 'POST':
        try:
            db.execute('DELETE FROM user WHERE id = ?', (user_id,))
            db.commit()
        except db.IntegrityError:
            error = 'Error deleting user.'
        else:
            flash('User deleted successfully.')
            return redirect(url_for('main.home'))

    return redirect(url_for('main.home', user_id=user_id, error=error))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user_data = get_db().execute(
            'SELECT id, username, is_admin FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        if user_data:
            g.user = {
                'id': user_data['id'],
                'username': user_data['username'],
                'is_admin': user_data['is_admin'],
            }
        else:
            g.user = None

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view