-- Database Triggers for Student Management System
USE student_management_db;

DROP TRIGGER IF EXISTS trg_auto_grade_before_insert;
DROP TRIGGER IF EXISTS trg_auto_grade_before_update;
DROP TRIGGER IF EXISTS trg_log_mark_change;

-- Audit Table for Mark Changes
CREATE TABLE IF NOT EXISTS marks_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    mark_id INT,
    old_internal DECIMAL(5,2),
    new_internal DECIMAL(5,2),
    old_external DECIMAL(5,2),
    new_external DECIMAL(5,2),
    changed_by_lecturer INT,
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

-- 1. Trigger to Auto-calculate Grade before insert/update
CREATE TRIGGER trg_auto_grade_before_insert
BEFORE INSERT ON marks
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(5,2);
    SET total = NEW.internal_marks + NEW.external_marks;
    
    SET NEW.grade = CASE 
        WHEN total >= 90 THEN 'O'
        WHEN total >= 80 THEN 'A+'
        WHEN total >= 70 THEN 'A'
        WHEN total >= 60 THEN 'B'
        WHEN total >= 50 THEN 'C'
        WHEN total >= 40 THEN 'P'
        ELSE 'F'
    END;
END //

CREATE TRIGGER trg_auto_grade_before_update
BEFORE UPDATE ON marks
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(5,2);
    SET total = NEW.internal_marks + NEW.external_marks;
    
    SET NEW.grade = CASE 
        WHEN total >= 90 THEN 'O'
        WHEN total >= 80 THEN 'A+'
        WHEN total >= 70 THEN 'A'
        WHEN total >= 60 THEN 'B'
        WHEN total >= 50 THEN 'C'
        WHEN total >= 40 THEN 'P'
        ELSE 'F'
    END;
END //

-- 2. Trigger to Log Mark Changes
CREATE TRIGGER trg_log_mark_change
AFTER UPDATE ON marks
FOR EACH ROW
BEGIN
    IF OLD.internal_marks <> NEW.internal_marks OR OLD.external_marks <> NEW.external_marks THEN
        INSERT INTO marks_audit (mark_id, old_internal, new_internal, old_external, new_external, changed_by_lecturer)
        VALUES (OLD.mark_id, OLD.internal_marks, NEW.internal_marks, OLD.external_marks, NEW.external_marks, NEW.lecturer_id);
    END IF;
END //

DELIMITER ;
