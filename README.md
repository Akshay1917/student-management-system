# 🎓 Student Management System (SMS)

A modern **Full Stack Student Management System** built using **Python Flask, MySQL, HTML, CSS, and JavaScript**.

This project helps educational institutions efficiently manage:
- Students
- Lecturers
- Subjects
- Marks
- Reports
- Authentication
- Excel/CSV uploads

---

## 🚀 Features

### 👨‍🎓 Student Module
- Student Registration & Login
- Secure Authentication
- View Profile
- View Subject-wise Marks
- Performance Dashboard
- Download Marks Card PDF
- Radar Chart Analysis

---

### 👨‍🏫 Lecturer Module
- Lecturer Registration & Login
- Add/Edit/Delete Students
- Subject Management
- Upload Marks via Excel/CSV
- Dashboard Analytics
- Export Reports

---

### 📊 Analytics & Reports
Built using **Chart.js**
- Bar Chart → Subject Averages
- Pie Chart → Grade Distribution
- Radar Chart → Student Performance
- Line Chart → Monthly Trends

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python Flask | Backend |
| MySQL | Database |
| HTML5 | Frontend |
| CSS3 | Styling |
| JavaScript | Client-side Logic |
| Chart.js | Charts |
| openpyxl | Excel Processing |
| reportlab | PDF Generation |
| bcrypt | Password Hashing |

---

# 📂 Project Structure

```bash
sms-project/
│
├── app.py
├── config.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── student/
│   └── lecturer/
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── routes/
│   ├── auth.py
│   ├── student.py
│   └── lecturer.py
│
├── models/
│   ├── db.py
│   └── queries.py
│
├── utils/
│   └── excel_parser.py
│
└── sql/
    ├── schema.sql
    ├── procedures.sql
    ├── triggers.sql
    ├── views.sql
    └── sample_data.sql
```

---

# 🗄️ Database Features

## Tables
- students
- lecturers
- subjects
- marks
- auth

---

## SQL Concepts Used
✅ Primary Keys  
✅ Foreign Keys  
✅ JOIN Queries  
✅ Aggregate Functions  
✅ Subqueries  
✅ Stored Procedures  
✅ Triggers  
✅ Views  
✅ Indexing  
✅ Normalization (3NF)

---

# ⚡ Stored Procedures

- `sp_upsert_mark`
- `sp_get_student_report`
- `sp_subject_statistics`
- `sp_bulk_import_marks`

---

# 🔥 Triggers

- `trg_auto_grade`
- `trg_log_mark_change`
- `trg_prevent_duplicate_usn`

---

# 📈 Views

- `vw_student_marks`
- `vw_subject_averages`
- `vw_student_summary`
- `vw_top_performers`

---

# 📥 Excel / CSV Upload

Lecturers can upload:
- `.xlsx`
- `.csv`

### Validation Features
- USN validation
- Subject code validation
- Marks validation
- Duplicate handling
- Error reporting
- Transaction rollback

---

# 🔐 Authentication & Security

- bcrypt Password Hashing
- Session Management
- Role-Based Authentication
- CSRF Protection
- Secure Routes

---

# 🎨 UI Features

- Responsive Design
- Mobile Friendly
- Dashboard Cards
- Interactive Charts
- Modern UI
- Flexbox & Grid Layouts

---

# 📦 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Akshay1917/student-management-system.git
cd student-management-system
```

---

## 2️⃣ Create Database

```sql
CREATE DATABASE sms_db;
```

---

## 3️⃣ Import SQL Files

Run in this order:

```bash
schema.sql
procedures.sql
triggers.sql
views.sql
sample_data.sql
```

---

## 4️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Configure Database

Update `config.py`

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'sms_db'
SECRET_KEY = 'your_secret_key'
```

---

## 7️⃣ Run Application

```bash
python app.py
```

Open browser:

```bash
http://localhost:5000
```

---

# 🔑 Sample Login Credentials

## Lecturer

| Email | Password |
|---|---|
| dr.sharma@sms.edu | Lecturer@123 |

---

## Student

| Email | Password |
|---|---|
| ravi@sms.edu | Student@123 |

---

# 📸 Screenshots

## 🏠 Home Page
_Add screenshot here_

## 👨‍🏫 Lecturer Dashboard
_Add screenshot here_

## 👨‍🎓 Student Dashboard
_Add screenshot here_

## 📤 Upload Marks Page
_Add screenshot here_

---

# 🌟 Future Improvements

- Attendance Management
- Admin Dashboard
- Email Notifications
- Password Reset
- JWT Authentication
- Cloud Deployment

---

# 📚 Learning Outcomes

This project demonstrates:
- Full Stack Development
- Database Design
- SQL Programming
- Authentication Systems
- File Processing
- Report Generation
- Data Visualization

---

# 🤝 Contributing

Contributions are welcome!

Fork the repository and submit a pull request.

---

# 📄 License

This project is developed for educational purposes.

---

# 👨‍💻 Author

## Akshay V

GitHub: https://github.com/Akshay1917

---

# ⭐ Support

If you like this project, give it a ⭐ on GitHub!
