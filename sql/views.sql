-- Database Views for Student Management System
USE student_management_db;

-- 1. View for Detailed Student Marks
CREATE OR REPLACE VIEW vw_student_marks AS
SELECT 
    s.usn,
    s.first_name,
    s.last_name,
    sub.subject_code,
    sub.subject_name,
    m.internal_marks,
    m.external_marks,
    m.total_marks,
    m.grade,
    m.semester,
    l.first_name as lecturer_name
FROM marks m
JOIN students s ON m.student_id = s.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
JOIN lecturers l ON m.lecturer_id = l.lecturer_id;

-- 2. View for Subject Averages
CREATE OR REPLACE VIEW vw_subject_averages AS
SELECT 
    sub.subject_code,
    sub.subject_name,
    AVG(m.total_marks) as avg_marks,
    COUNT(m.student_id) as student_count,
    MIN(m.total_marks) as min_marks,
    MAX(m.total_marks) as max_marks
FROM marks m
JOIN subjects sub ON m.subject_id = sub.subject_id
GROUP BY sub.subject_id;

-- 3. View for Student Summary (GPA-like calculation)
CREATE OR REPLACE VIEW vw_student_summary AS
SELECT 
    s.student_id,
    s.usn,
    s.first_name,
    s.last_name,
    COUNT(m.subject_id) as subjects_taken,
    SUM(m.total_marks) as total_score,
    AVG(m.total_marks) as average_score,
    CASE 
        WHEN AVG(m.total_marks) >= 90 THEN 'O'
        WHEN AVG(m.total_marks) >= 80 THEN 'A+'
        WHEN AVG(m.total_marks) >= 70 THEN 'A'
        WHEN AVG(m.total_marks) >= 60 THEN 'B'
        ELSE 'F'
    END as overall_grade
FROM students s
LEFT JOIN marks m ON s.student_id = m.student_id
GROUP BY s.student_id;

-- 4. View for Top Performers per Subject
CREATE OR REPLACE VIEW vw_top_performers AS
SELECT 
    sub.subject_name,
    s.first_name,
    s.last_name,
    m.total_marks
FROM marks m
JOIN students s ON m.student_id = s.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
WHERE m.total_marks = (SELECT MAX(total_marks) FROM marks WHERE subject_id = sub.subject_id);
