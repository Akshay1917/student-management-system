from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models.queries import Queries
from functools import wraps
from utils.excel_parser import FileParser
import os
from werkzeug.utils import secure_filename

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
            
    return render_template('lecturer/upload_marks.html')

@lecturer_bp.route('/reports')
@lecturer_required
def reports():
    marks = Queries.execute_query("SELECT * FROM vw_student_marks", fetchall=True)
    return render_template('lecturer/reports.html', marks=marks)
