from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.queries import Queries
from functools import wraps
from routes.auth import bcrypt

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.student_login')) # Or generic login
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        'students': Queries.execute_query("SELECT COUNT(*) as count FROM students", fetchone=True)['count'],
        'lecturers': Queries.execute_query("SELECT COUNT(*) as count FROM lecturers", fetchone=True)['count'],
        'subjects': Queries.execute_query("SELECT COUNT(*) as count FROM subjects", fetchone=True)['count'],
        'total_marks': Queries.execute_query("SELECT COUNT(*) as count FROM marks", fetchone=True)['count']
    }
    return render_template('admin/dashboard.html', stats=stats)

# --- Student Management ---
@admin_bp.route('/students')
@admin_required
def manage_students():
    students = Queries.execute_query("SELECT * FROM students", fetchall=True)
    return render_template('admin/manage_students.html', students=students)

@admin_bp.route('/students/add', methods=['POST'])
@admin_required
def add_student():
    usn = request.form.get('usn')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    course = request.form.get('course')
    semester = request.form.get('semester')
    password = request.form.get('password', 'password123')
    
    try:
        # 1. Add to students table
        student_id = Queries.execute_query(
            "INSERT INTO students (usn, first_name, last_name, email, course, semester) VALUES (%s, %s, %s, %s, %s, %s)",
            (usn, first_name, last_name, email, course, semester)
        )
        
        # 2. Add to auth table
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        Queries.execute_query(
            "INSERT INTO auth (username, password_hash, role, user_id) VALUES (%s, %s, %s, %s)",
            (usn, password_hash, 'student', student_id)
        )
        
        flash(f'Student {usn} added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding student: {str(e)}', 'error')
        
    return redirect(url_for('admin.manage_students'))

@admin_bp.route('/students/delete/<int:id>')
@admin_required
def delete_student(id):
    try:
        # Get USN first to remove from auth
        student = Queries.execute_query("SELECT usn FROM students WHERE student_id = %s", (id,), fetchone=True)
        if student:
            Queries.execute_query("DELETE FROM auth WHERE username = %s AND role = 'student'", (student['usn'],))
            Queries.execute_query("DELETE FROM students WHERE student_id = %s", (id,))
            flash('Student deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')
    return redirect(url_for('admin.manage_students'))

# --- Lecturer Management ---
@admin_bp.route('/lecturers')
@admin_required
def manage_lecturers():
    lecturers = Queries.execute_query("SELECT * FROM lecturers", fetchall=True)
    return render_template('admin/manage_lecturers.html', lecturers=lecturers)

@admin_bp.route('/lecturers/add', methods=['POST'])
@admin_required
def add_lecturer():
    emp_id = request.form.get('employee_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    dept = request.form.get('department')
    password = request.form.get('password', 'password123')
    
    try:
        lecturer_id = Queries.execute_query(
            "INSERT INTO lecturers (employee_id, first_name, last_name, email, department) VALUES (%s, %s, %s, %s, %s)",
            (emp_id, first_name, last_name, email, dept)
        )
        
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        Queries.execute_query(
            "INSERT INTO auth (username, password_hash, role, user_id) VALUES (%s, %s, %s, %s)",
            (emp_id, password_hash, 'lecturer', lecturer_id)
        )
        
        flash(f'Lecturer {emp_id} added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding lecturer: {str(e)}', 'error')
        
    return redirect(url_for('admin.manage_lecturers'))

# --- Subject Management ---
@admin_bp.route('/subjects')
@admin_required
def manage_subjects():
    subjects = Queries.execute_query("SELECT * FROM subjects", fetchall=True)
    return render_template('admin/manage_subjects.html', subjects=subjects)

@admin_bp.route('/subjects/add', methods=['POST'])
@admin_required
def add_subject():
    code = request.form.get('subject_code')
    name = request.form.get('subject_name')
    credits = request.form.get('credits')
    dept = request.form.get('department')
    
    try:
        Queries.execute_query(
            "INSERT INTO subjects (subject_code, subject_name, credits, department) VALUES (%s, %s, %s, %s)",
            (code, name, credits, dept)
        )
        flash(f'Subject {code} added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding subject: {str(e)}', 'error')
        
    return redirect(url_for('admin.manage_subjects'))
