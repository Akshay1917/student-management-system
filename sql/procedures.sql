-- Stored Procedures for Student Management System
USE student_management_db;

DROP PROCEDURE IF EXISTS sp_upsert_mark;
DROP PROCEDURE IF EXISTS sp_get_student_report;
DROP PROCEDURE IF EXISTS sp_subject_statistics;

DELIMITER //

-- 1. Procedure to Upsert Marks
CREATE PROCEDURE sp_upsert_mark(
    IN p_usn VARCHAR(20),
    IN p_subject_code VARCHAR(20),
    IN p_lecturer_id INT,
    IN p_internal DECIMAL(5,2),
    IN p_external DECIMAL(5,2),
    IN p_semester INT,
    IN p_academic_year VARCHAR(10)
)
BEGIN
    DECLARE v_student_id INT;
    DECLARE v_subject_id INT;
    
    -- Get Student ID
    SELECT student_id INTO v_student_id FROM students WHERE usn = p_usn;
    
    -- Get Subject ID
    SELECT subject_id INTO v_subject_id FROM subjects WHERE subject_code = p_subject_code;
    
    IF v_student_id IS NOT NULL AND v_subject_id IS NOT NULL THEN
        INSERT INTO marks (student_id, subject_id, lecturer_id, internal_marks, external_marks, semester, academic_year)
        VALUES (v_student_id, v_subject_id, p_lecturer_id, p_internal, p_external, p_semester, p_academic_year)
        ON DUPLICATE KEY UPDATE 
            internal_marks = p_internal,
            external_marks = p_external,
            lecturer_id = p_lecturer_id,
            semester = p_semester;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student or Subject not found';
    END IF;
END //

-- 2. Procedure to Get Student Report Card
CREATE PROCEDURE sp_get_student_report(IN p_usn VARCHAR(20))
BEGIN
    SELECT * FROM vw_student_marks WHERE usn = p_usn;
END //

-- 3. Procedure for Subject Statistics
CREATE PROCEDURE sp_subject_statistics(IN p_subject_code VARCHAR(20))
BEGIN
    SELECT * FROM vw_subject_averages WHERE subject_code = p_subject_code;
END //

DELIMITER ;
