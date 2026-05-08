-- Sample Data for Student Management System
USE student_management_db;

-- 1. Insert Sample Lecturers
INSERT IGNORE INTO lecturers (employee_id, first_name, last_name, email, department) VALUES
('L001', 'John', 'Doe', 'john.doe@university.edu', 'Computer Science'),
('L002', 'Jane', 'Smith', 'jane.smith@university.edu', 'Mathematics');

-- 2. Insert Sample Students
INSERT IGNORE INTO students (usn, first_name, last_name, email, phone, course, semester) VALUES
('S001', 'Alice', 'Johnson', 'alice@student.edu', '1234567890', 'B.Tech CS', 4),
('S002', 'Bob', 'Brown', 'bob@student.edu', '9876543210', 'B.Tech CS', 4);

-- 3. Insert Sample Subjects
INSERT IGNORE INTO subjects (subject_code, subject_name, credits, department) VALUES
('CS401', 'Database Management Systems', 4, 'Computer Science'),
('CS402', 'Operating Systems', 4, 'Computer Science'),
('MA401', 'Discrete Mathematics', 3, 'Mathematics');

-- 4. Insert Sample Auth (Password is 'password123' hashed with bcrypt)
INSERT IGNORE INTO auth (username, password_hash, role, user_id) VALUES
('L001', '$2b$12$VEDXW8UYBsUtVMVTj5xVcupJxr4bmtyxoKgexSzLKAP03yGANzCeG', 'lecturer', 1),
('S001', '$2b$12$VEDXW8UYBsUtVMVTj5xVcupJxr4bmtyxoKgexSzLKAP03yGANzCeG', 'student', 1);

-- 5. Insert Sample Marks
INSERT IGNORE INTO marks (student_id, subject_id, lecturer_id, internal_marks, external_marks, semester, academic_year) VALUES
(1, 1, 1, 25.00, 60.00, 4, '2023-24'),
(1, 2, 1, 22.00, 55.00, 4, '2023-24'),
(2, 1, 1, 28.00, 62.00, 4, '2023-24');
