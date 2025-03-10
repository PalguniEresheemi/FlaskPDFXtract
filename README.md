Project : Flask PDF Extractor

Description:
Flask PDF Extractor is a web application that allows users to upload PDF documents, extract their textual content while maintaining the original formatting, and provides RESTful API endpoints for seamless integration with frontend applications. This project integrates PostgreSQL as its database to manage user data, file records, and extraction history.

Features:
User Authentication: Secure login and registration system with password hashing.
PDF Upload: Users can upload PDFs for text extraction.
Text Extraction: Extracts text from PDFs while preserving layout and structure.
PostgreSQL Integration: Efficient storage of user details, uploaded files, and extracted text.
API Endpoints: Provides API endpoints for uploading PDFs, retrieving extracted text, and managing user data.


Project Structure

/Flask_PDF_Extractor
|--/static
|--/templates
|   |-- extracted_text.html
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- upload.html
|-- /uploads
|-- config.py
|-- requirements.txt
|-- app.py
|-- README.md
|--database.db

Setup Instructions:

* Clone the Repository
git clone <https://github.com/PalguniEresheemi/FlaskPDFXtract.git>
cd Flask_PDF_Extractor

* Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

* Install Dependencies
pip install -r requirements.txt

* Configure PostgreSQL Database
Install PostgreSQL if not already installed.

* Create a database called pdf_extractor_db.
Update config.py with database credentials:
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/pdf_extractor_db'

* Apply Database Migrations
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

* Run the Application
python run.py

* Access the Web Application:
Visit http://localhost:5000 in your browser.

* API Endpoints:

Method              Endpoint                     Description
POST                /api/register                Register a new user.
POST                /api/login                   Authenticate a user.
POST                /api/upload                  Upload a PDF for extraction.
GET                 /api/extract/<file_id>       Retrieve extracted text.

* Future Enhancements
Implement user roles for better control over file management.
Enhance TTS functionality with language options.
Add PDF preview functionality before extraction.

* Contributing
Contributions are welcome! Feel free to fork the repository, create a branch, and submit a pull request.

* License
This project is licensed under the MIT License. See LICENSE for details.

