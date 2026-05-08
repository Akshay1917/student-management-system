import os
import mysql.connector
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask import Flask

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)

def update_hashes():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB'),
            port=os.getenv('MYSQL_PORT')
        )
        cursor = conn.cursor()
        
        new_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        print(f"Generated new hash for 'password123': {new_hash}")
        
        cursor.execute("UPDATE auth SET password_hash = %s", (new_hash,))
        conn.commit()
        
        print("Successfully updated all password hashes in the 'auth' table to 'password123'!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    update_hashes()
