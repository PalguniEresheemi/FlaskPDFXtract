import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:palguni814@localhost:5432/flask_pdf_app'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf'}
    SECRET_KEY = 'your_secret_key'  # Added for session management in Flask-Login
