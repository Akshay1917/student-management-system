# Student Management System

A Flask and MySQL based student management system for lecturer mark uploads, student dashboards, academic reports, and PDF report-card downloads.

## Features

- Student and lecturer login
- Student dashboard with marks, grade summary, and PDF report download
- Lecturer dashboard with student/subject statistics
- CSV and Excel mark upload
- MySQL schema, views, triggers, procedures, and sample data

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update your database credentials.
4. Run the SQL files in this order:

```text
sql/schema.sql
sql/triggers.sql
sql/views.sql
sql/procedures.sql
sql/sample_data.sql
```

5. Start the app:

```bash
python app.py
```

The app runs at `http://127.0.0.1:5000/` by default.

## Sample Login

After loading `sql/sample_data.sql`, use:

- Student: `S001` / `password123`
- Lecturer: `L001` / `password123`
