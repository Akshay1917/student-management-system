from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db
from routes.auth import auth_bp, bcrypt
from routes.lecturer import lecturer_bp
from routes.student import student_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lecturer_bp)
    app.register_blueprint(student_bp)

    @app.route('/')
    def index():
        if 'user_id' in session:
            if session.get('role') == 'student':
                return redirect(url_for('student.dashboard'))
            elif session.get('role') == 'lecturer':
                return redirect(url_for('lecturer.dashboard'))
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
