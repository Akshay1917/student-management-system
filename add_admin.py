import os
import mysql.connector
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask import Flask

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)

def add_admin():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            port=os.getenv('MYSQL_PORT')
        )
        cursor = conn.cursor()
        
        username = 'admin'
        password = 'admin123'
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Check if admin exists
        cursor.execute("SELECT * FROM auth WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Admin user already exists.")
        else:
            # For admin, user_id can be 0 or a dummy value since they aren't in students/lecturers table
            cursor.execute("INSERT INTO auth (username, password_hash, role, user_id) VALUES (%s, %s, %s, %s)",
                           (username, password_hash, 'admin', 0))
            conn.commit()
            print(f"Successfully added admin user: {username} / {password}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    add_admin()
