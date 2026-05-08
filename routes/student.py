from flask import Blueprint, render_template, session, redirect, url_for, flash, send_file, Response, request
from models.queries import Queries
from functools import wraps
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from routes.auth import bcrypt

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Student login required', 'error')
            return redirect(url_for('auth.student_login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@student_required
def dashboard():
    student_id = session['user_id']
    profile = Queries.get_student_profile(student_id)
    
    # Get marks for the student
    marks = Queries.execute_query("SELECT * FROM vw_student_marks WHERE usn = %s", (profile['usn'],), fetchall=True)
    
    # Get summary
    summary = Queries.execute_query("SELECT * FROM vw_student_summary WHERE student_id = %s", (student_id,), fetchone=True)
    
    return render_template('student/dashboard.html', profile=profile, marks=marks, summary=summary)

@student_bp.route('/download-report')
@student_required
def download_report():
    student_id = session['user_id']
    profile = Queries.get_student_profile(student_id)
    marks = Queries.execute_query("SELECT * FROM vw_student_marks WHERE usn = %s", (profile['usn'],), fetchall=True)
    summary = Queries.execute_query("SELECT * FROM vw_student_summary WHERE student_id = %s", (student_id,), fetchone=True)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(f"Academic Report Card - {profile['first_name']} {profile['last_name']}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Profile Info
    elements.append(Paragraph(f"USN: {profile['usn']}", styles['Normal']))
    elements.append(Paragraph(f"Course: {profile['course']}", styles['Normal']))
    elements.append(Paragraph(f"Semester: {profile['semester']}", styles['Normal']))
    elements.append(Paragraph(f"Overall Grade: {summary['overall_grade'] or 'N/A'}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Table
    data = [['Subject Code', 'Subject Name', 'Internal', 'External', 'Total', 'Grade']]
    for mark in marks:
        data.append([
            mark['subject_code'],
            mark['subject_name'],
            str(mark['internal_marks']),
            str(mark['external_marks']),
            str(mark['total_marks']),
            mark['grade']
        ])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Report_{profile['usn']}.pdf",
        mimetype='application/pdf'
    )

@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    student_id = session['user_id']
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        profile_pic = request.files.get('profile_pic')
        
        try:
            # 1. Update basic info
            Queries.execute_query(
                "UPDATE students SET email = %s, phone = %s WHERE student_id = %s",
                (email, phone, student_id)
            )
            
            # 2. Handle Profile Picture
            if profile_pic and profile_pic.filename:
                ext = os.path.splitext(profile_pic.filename)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:
                    filename = f"student_{student_id}{ext}"
                    filepath = os.path.join(current_app.config['PROFILE_PICS_FOLDER'], filename)
                    profile_pic.save(filepath)
                    Queries.execute_query(
                        "UPDATE students SET profile_pic = %s WHERE student_id = %s",
                        (filename, student_id)
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
            
        return redirect(url_for('student.profile'))
        
    profile_data = Queries.get_student_profile(student_id)
    return render_template('student/profile.html', profile=profile_data)
