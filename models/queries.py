from .db import Database
import mysql.connector

class Queries:
    @staticmethod
    def execute_query(query, params=(), fetchone=False, fetchall=False):
        db = Database.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            db.commit()
            return cursor.lastrowid
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()

    @staticmethod
    def call_procedure(proc_name, params=()):
        db = Database.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.callproc(proc_name, params)
            db.commit()
            # Procedures might return multiple result sets
            results = []
            for result in cursor.stored_results():
                results.append(result.fetchall())
            return results
        except Exception:
            db.rollback()
            raise
        finally:
            cursor.close()

    @staticmethod
    def get_user_by_username(username):
        query = "SELECT * FROM auth WHERE username = %s"
        return Queries.execute_query(query, (username,), fetchone=True)

    @staticmethod
    def get_student_profile(student_id):
        query = "SELECT * FROM students WHERE student_id = %s"
        return Queries.execute_query(query, (student_id,), fetchone=True)

    @staticmethod
    def get_lecturer_profile(lecturer_id):
        query = "SELECT * FROM lecturers WHERE lecturer_id = %s"
        return Queries.execute_query(query, (lecturer_id,), fetchone=True)

    @staticmethod
    def get_student_marks(usn):
        return Queries.call_procedure('sp_get_student_report', (usn,))
