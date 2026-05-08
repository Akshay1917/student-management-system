import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def update_schema():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            port=os.getenv('MYSQL_PORT')
        )
        cursor = conn.cursor()
        
        # Add profile_pic column to students
        try:
            cursor.execute("ALTER TABLE students ADD COLUMN profile_pic VARCHAR(255) DEFAULT 'default.png'")
            print("Added profile_pic to students table.")
        except Exception as e:
            print(f"Students table update: {e}")
            
        # Add profile_pic column to lecturers
        try:
            cursor.execute("ALTER TABLE lecturers ADD COLUMN profile_pic VARCHAR(255) DEFAULT 'default.png'")
            print("Added profile_pic to lecturers table.")
        except Exception as e:
            print(f"Lecturers table update: {e}")
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    update_schema()
