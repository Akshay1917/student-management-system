from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models.queries import Queries
from functools import wraps
from utils.excel_parser import FileParser
import os
from werkzeug.utils import secure_filename
from routes.auth import bcrypt

lecturer_bp = Blueprint('lecturer', __name__, url_prefix='/lecturer')

def lecturer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'lecturer':
            flash('Lecturer login required', 'error')
            return redirect(url_for('auth.lecturer_login'))
        return f(*args, **kwargs)
    return decorated_function

@lecturer_bp.route('/dashboard')
@lecturer_required
def dashboard():
    lecturer_id = session['user_id']
    profile = Queries.get_lecturer_profile(lecturer_id)
    
    # Get some stats for the dashboard
    stats = {
        'total_students': Queries.execute_query("SELECT COUNT(*) as count FROM students", fetchone=True)['count'],
        'total_subjects': Queries.execute_query("SELECT COUNT(*) as count FROM subjects", fetchone=True)['count'],
        'recent_marks': Queries.execute_query("SELECT * FROM vw_student_marks LIMIT 5", fetchall=True)
    }
    
    return render_template('lecturer/dashboard.html', profile=profile, stats=stats)

@lecturer_bp.route('/upload', methods=['GET', 'POST'])
@lecturer_required
def upload_marks():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        ext = os.path.splitext(file.filename)[1].lower()
        if file and ext in ('.csv', '.xlsx'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Parse file
                if ext == '.csv':
                    data = FileParser.parse_csv(filepath)
                else:
                    data = FileParser.parse_excel(filepath)
                
                # Validate data
                errors = FileParser.validate_marks_data(data)
                if errors:
                    for error in errors[:5]: # Show first 5 errors
                        flash(error, 'error')
                    return redirect(request.url)
                
                lecturer_id = session['user_id']
                success_count = 0
                
                for row in data:
                    try:
                        Queries.call_procedure('sp_upsert_mark', (
                            row['usn'],
                            row['subject_code'],
                            lecturer_id,
                            float(row['internal_marks']),
                            float(row['external_marks']),
                            int(row['semester']),
                            str(row['academic_year'])
                        ))
                        success_count += 1
                    except Exception as e:
                        print(f"Error processing row: {e}")
                
                flash(f'Successfully processed {success_count} records.', 'success')
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            return redirect(url_for('lecturer.dashboard'))

        flash('Invalid file type. Please upload a CSV or Excel file.', 'error')
        return redirect(request.url)
            
    # Fetch students and subjects for manual entry
    students = Queries.execute_query("SELECT usn, first_name, last_name FROM students", fetchall=True)
    subjects = Queries.execute_query("SELECT subject_code, subject_name FROM subjects", fetchall=True)
            
    return render_template('lecturer/upload_marks.html', students=students, subjects=subjects)

@lecturer_bp.route('/manual-entry', methods=['POST'])
@lecturer_required
def submit_mark_manual():
    usn = request.form.get('usn')
    subject_code = request.form.get('subject_code')
    internal = request.form.get('internal_marks')
    external = request.form.get('external_marks')
    semester = request.form.get('semester')
    academic_year = request.form.get('academic_year')
    lecturer_id = session['user_id']
    
    try:
        Queries.call_procedure('sp_upsert_mark', (
            usn,
            subject_code,
            lecturer_id,
            float(internal),
            float(external),
            int(semester),
            str(academic_year)
        ))
        flash(f'Mark for {usn} updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating mark: {str(e)}', 'error')
        
    return redirect(url_for('lecturer.upload_marks'))

@lecturer_bp.route('/reports')
@lecturer_required
def reports():
    marks = Queries.execute_query("SELECT * FROM vw_student_marks", fetchall=True)
    return render_template('lecturer/reports.html', marks=marks)

@lecturer_bp.route('/profile', methods=['GET', 'POST'])
@lecturer_required
def profile():
    lecturer_id = session['user_id']
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        profile_pic = request.files.get('profile_pic')
        
        try:
            # 1. Update basic info
            Queries.execute_query(
                "UPDATE lecturers SET email = %s WHERE lecturer_id = %s",
                (email, lecturer_id)
            )
            
            # 2. Handle Profile Picture
            if profile_pic and profile_pic.filename:
                ext = os.path.splitext(profile_pic.filename)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:
                    filename = f"lecturer_{lecturer_id}{ext}"
                    filepath = os.path.join(current_app.config['PROFILE_PICS_FOLDER'], filename)
                    profile_pic.save(filepath)
                    Queries.execute_query(
                        "UPDATE lecturers SET profile_pic = %s WHERE lecturer_id = %s",
                        (filename, lecturer_id)
                    )
                else:
                    flash('Invalid image format. Use JPG or PNG.', 'warning')
            
            # 2. Update password if requested
            if new_password and current_password:
                user = Queries.get_user_by_username(session['username'])
                if bcrypt.check_password_hash(user['password_hash'], current_password):
                    new_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    Queries.execute_query(
                        "UPDATE auth SET password_hash = %s WHERE auth_id = %s",
                        (new_hash, session['auth_id'])
                    )
                    flash('Profile and password updated successfully!', 'success')
                else:
                    flash('Current password incorrect. Info updated, but password remains unchanged.', 'warning')
            else:
                flash('Profile updated successfully!', 'success')
                
        except Exception as e:
            flash(f'Error updating profile: {str(e)}', 'error')
            
        return redirect(url_for('lecturer.profile'))
        
    profile_data = Queries.get_lecturer_profile(lecturer_id)
    return render_template('lecturer/profile.html', profile=profile_data)
