from flask import Flask, render_template, redirect, url_for, flash, request, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF for PDF parsing

# Initialize Flask App
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# ---------------------------
# Database Models
# ---------------------------

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

# Extracted Text Model
class ExtractedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

# ---------------------------
# User Authentication
# ---------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('upload_pdf'))
        else:
            flash('Invalid credentials!', 'danger')
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# ---------------------------
# File Upload & Extraction Logic
# ---------------------------

# File Upload Route
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_pdf():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text
            text = extract_text_from_pdf(filepath)

            # Save extracted text to database
            new_entry = ExtractedData(filename=filename, content=text)
            db.session.add(new_entry)
            db.session.commit()

            flash('File uploaded and text extracted successfully!', 'success')
            return render_template('extracted_text.html', text=text)
    
    return render_template('upload.html')

# Extract text from PDF
def extract_text_from_pdf(filepath):
    try:
        doc = fitz.open(filepath)
        text = "\n".join(page.get_text() for page in doc)
        return text.strip() if text.strip() else "No text found in PDF."
    except Exception as e:
        return f"Error extracting text: {e}"

# ---------------------------
# View Extracted Data
# ---------------------------

@app.route('/extracted_data', methods=['GET'])
@login_required
def view_extracted_data():
    data = ExtractedData.query.all()
    return render_template('extracted_data.html', data=data)

# ---------------------------
# Database Creation
# ---------------------------

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True)
