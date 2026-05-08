import os
import mysql.connector
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask import Flask

load_dotenv()

def check_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            port=os.getenv('MYSQL_PORT')
        )
        cursor = conn.cursor(dictionary=True)
        print("Successfully connected to the database!")
        
        cursor.execute("SELECT * FROM auth")
        users = cursor.fetchall()
        
        if not users:
            print("WARNING: The 'auth' table is empty. Did you run sample_data.sql?")
        else:
            print(f"Found {len(users)} users in 'auth' table:")
            for user in users:
                print(f" - Username: {user['username']}, Role: {user['role']}")
                
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_db()
