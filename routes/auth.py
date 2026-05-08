from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from models.queries import Queries

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/login/student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Queries.get_user_by_username(username)
        
        if user and user['role'] == 'student' and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['auth_id'] = user['auth_id']
            session['username'] = user['username']
            session['role'] = 'student'
            flash('Login successful!', 'success')
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid USN or password', 'error')
            
    return render_template('student/login.html')

@auth_bp.route('/login/lecturer', methods=['GET', 'POST'])
def lecturer_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Queries.get_user_by_username(username)
        
        if user and user['role'] == 'lecturer' and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['auth_id'] = user['auth_id']
            session['username'] = user['username']
            session['role'] = 'lecturer'
            flash('Login successful!', 'success')
            return redirect(url_for('lecturer.dashboard'))
        else:
            flash('Invalid Employee ID or password', 'error')
            
    return render_template('lecturer/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))
