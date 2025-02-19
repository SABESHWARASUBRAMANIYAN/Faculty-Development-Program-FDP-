import pytesseract
import os
from PIL import Image
from flask import Flask, render_template, request, redirect,flash,url_for,session,send_file,send_from_directory,jsonify,Response,make_response

from flask_sqlalchemy import SQLAlchemy
import random
import string
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
#try jupy
import subprocess
import csv
from io import StringIO
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import text 
import io
import sqlite3
import re
app = Flask(__name__)
app.debug = True
app = Flask(__name__)
app.debug = True
app.secret_key = 'Dhava1511' 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dhavadhava1511@gmail.com'
app.config['MAIL_PASSWORD'] = 'fnudzmrgftsdbtay'
app.config['MAIL_DEFAULT_SENDER'] = 'dhavasri@gmail.com'
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(50)) 
    staffid = db.Column(db.Integer)
    password = db.Column(db.String(255))
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    designation = db.Column(db.String(100))
    company = db.Column(db.String(100))
    password_reset_token = db.Column(db.String(100))
class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.staffid'), nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)  
    login_time = db.Column(db.DateTime, nullable=False)
    logout_time = db.Column(db.DateTime)
    user = db.relationship('User', backref='login_history')  
class Data(db.Model):
    __tablename__='extracted_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    certificate_type = db.Column(db.String(100))
    date = db.Column(db.String(20))
    def __repr__(self):
        return f"Data('{self.name}','{self.certificate_type}','{self.date}')"   
class FDP_Attended(db.Model):
    __tablename__ = 'fdp_attended'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    programme_attended = db.Column(db.String(100))
    from_date = db.Column(db.String(20))
    to_date = db.Column(db.String(20))
    organizer = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))
    no_of_days = db.Column(db.String(10))
class FDP_Conducted(db.Model):
    __tablename__ = 'fdp_conducted'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    programme_conducted = db.Column(db.String(100))
    from_date = db.Column(db.String(20))
    to_date = db.Column(db.String(20))
    organizer = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))
    no_of_days = db.Column(db.String(10))
class CONFERENCE_Conducted(db.Model):
    __tablename__ = 'conference_conducted'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    programme_conducted= db.Column(db.String(100))
    from_date = db.Column(db.String(20))
    to_date = db.Column(db.String(20))
    organizer = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))
    no_of_days = db.Column(db.String(100))
class CONFERENCE_Attended(db.Model):
    __tablename__ = 'conference_attended'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    programme_attended = db.Column(db.String(100))
    from_date = db.Column(db.String(20))
    to_date = db.Column(db.String(20))
    organizer = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))
    no_of_days = db.Column(db.String(100))
class LECTURES_Conducted(db.Model):
    __tablename__ = 'lectures_conducted'
    id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    department = db.Column(db.String(100))
    programme_conducted = db.Column(db.String(100))
    from_date = db.Column(db.String(20))
    to_date = db.Column(db.String(20))
    organizer = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))
    no_of_days = db.Column(db.String(100))
with app.app_context():
    db.create_all()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(image, lang='eng', config=custom_config)    
        return extracted_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
@app.route('/fdp', methods=['GET', 'POST'])
def fdp():
    if request.method == 'POST':
        fdp_file = request.files['fdpFile']
        if fdp_file:
            filename = secure_filename(fdp_file.filename)
            fdp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            fdp_file.save(fdp_file_path)
            extracted_text = extract_text_from_image(fdp_file_path)
            name = None
            certificate_type = None
            month = None
            month_mapping = None
            year = None
            if extracted_text:
                if re.search(r'IoT Technologies and Analytics', extracted_text, re.I):
                    certificate_type = 'FDP Conducted'
                    if re.search(r'Dr\. (.+?),', extracted_text):
                        name = re.search(r'Dr\. (.+?),', extracted_text).group(1).strip()
                    else:
                        name = "Not Found"
                    if re.search(r'Department of (.+?)\n', extracted_text):
                        department = re.search(r'Department of (.+?)\n', extracted_text).group(1).strip()
                    else:
                        department = "Not Found"
                    designation_pattern = r"Dr\. .*?,\s(.*?)\s\(Sr\. Gr\.\)"
                    designation_match = re.search(designation_pattern, extracted_text)
                    designation = designation_match.group(1).strip() if designation_match else "Not Found"
                    programme_conducted_match = re.search( r"on\s\|\s(.*?)\s\|", extracted_text)
                    programme_conducted = programme_conducted_match.group(1).strip() if programme_conducted_match else "Not Found"
                    date_match = re.search(r'from (\d{2}/\d{2}/\d{4}) ag (\d{2}/\d{2}/\d{4})', extracted_text)
                    if date_match:
                        from_date = date_match.group(1).strip()
                        to_date = date_match.group(2).strip()
                    else:
                        from_date = "Not Found"
                        to_date = "Not Found"
                    if re.search(r'sponsored by (.+?) & organised by (.+)', extracted_text):
                        sponsor = re.search(r'sponsored by (.+?) & organised by (.+)', extracted_text).group(1).strip()
                        organizer = re.search(r'sponsored by (.+?) & organised by (.+)', extracted_text).group(2).strip()
                    else:
                        organizer = "Not Found"
                        sponsor = "Not Found"
                    if from_date != "Not Found" and to_date != "Not Found":
                        no_of_days = str((datetime.strptime(to_date, '%d/%m/%Y') - datetime.strptime(from_date, '%d/%m/%Y')).days + 1)
                    else:
                        no_of_days = "Not Found"     
                elif re.search(r'CERTIFICATE OF PARTICIPATION', extracted_text, re.I):
                    certificate_type = 'FDP Attended'                 
                    if re.search(r"certify that Dr (.+?),", extracted_text):
                        name = re.search(r"certify that Dr (.+?),", extracted_text).group(1).strip()
                    else:
                        name = "Not Found"
                    if re.search(r"([A-Za-z\s]+Professor)", extracted_text):
                        designation = re.search(r"([A-Za-z\s]+Professor)", extracted_text).group(1).strip()
                    else:
                        designation = "Not Found"
                    if re.search(r"Department\s+of\s+([A-Za-z\s]+)", extracted_text):
                        department = re.search(r"Department\s+of\s+([A-Za-z\s]+)", extracted_text).group(1).strip()
                    else:
                        department = "Not Found"
                    if re.search(r'(\d+\s+Days\s+[A-Za-z\s]+Programme)', extracted_text):
                        programme_attended = re.search(r'(\d+\s+Days\s+[A-Za-z\s]+Programme)', extracted_text).group(1).strip()
                    else:
                        programme_attended = "Not Found"
                    date_match = re.search(r'from\s(\d{2}-\d{2}-\d{4})\sto\s(\d{2}-\d{2}-\d{4})', extracted_text)
                    if date_match:
                        from_date = date_match.group(1).strip()
                        to_date = date_match.group(2).strip()
                    else:
                        from_date = "Not Found"
                        to_date = "Not Found"
                    organizer_match = re.search(r"Department\s+of\s+([A-Za-z\s]+)", extracted_text)
                    if organizer_match:
                        organizer = organizer_match.group(1).strip()
                    else:
                        organizer = "Not Found"
                    sponsor_match = re.search(r'in association with ([^.]+)\.', extracted_text)
                    if sponsor_match:
                        sponsor = sponsor_match.group(1).strip()
                    else:
                        sponsor = "Not Found"
                    # Calculate no of days (assuming from_date and to_date are in the correct format)
                    if from_date != "Not Found" and to_date != "Not Found":
                        no_of_days = str((datetime.strptime(to_date, '%d-%m-%Y') - datetime.strptime(from_date, '%d-%m-%Y')).days + 1)
                    else:
                        no_of_days = "Not Found"     
                elif re.search(r'Virtual International Conference of Chemistry', extracted_text, re.I):
                    certificate_type = 'CONFERENCE Attended'
                    if re.search(r'Dr\.\s(.+?)\sFor\sattendance', extracted_text):
                        name = re.search(r'Dr\.\s(.+?)\sFor\sattendance', extracted_text).group(1).strip()
                    else:
                        name = "Not Found"
                    designation_match = re.search(r'Dr\.', extracted_text)
                    if designation_match:
                        designation = designation_match.group(0).strip()
                    else:
                        designation = "Not Found"
                    if re.search(r'Organized by Department of (.+?),', extracted_text):
                        department = re.search(r'Organized by Department of (.+?),', extracted_text).group(1).strip()
                    else:
                        department = "Not Found"
                    if re.search(r'(\d+"\s[A-Za-z\s]+)', extracted_text):
                        programme_attended = re.search(r'(\d+"\s[A-Za-z\s]+)', extracted_text).group(0)
                    else:
                        programme_attended = "Not Found"
                    if re.search(r'(Department of [A-Za-z\s,]+)', extracted_text):
                        organizer = re.search(r'(Department of [A-Za-z\s,]+)', extracted_text).group(1).strip()
                    else:
                        organizer = "Not Found"
                    if re.search(r'Organized by (.*?) \d{1,2}-\d{1,2} [A-Za-z]+ \d{4}', extracted_text):
                        sponsor = re.search(r'Organized by (.*?) \d{1,2}-\d{1,2} [A-Za-z]+ \d{4}', extracted_text).group(1).strip()
                    else:
                        sponsor = "Not Found"
                    date_pattern = r'(\d{1,2}-\d{1,2}\s\w+\s\d{4})'
                    months=None
                    date_matches = re.findall(date_pattern, extracted_text)

                    # Check if there are at least two date matches (from_date and to_date)
                    if len(date_matches) >= 2:
                        from_date = date_matches[0]  # The first match is from_date
                        to_date = date_matches[1]    # The second match is to_date
                        
                        # Calculate the number of days based on the date difference
                        from_date_parts = from_date.split()
                        to_date_parts = to_date.split()
                        from_day, from_month, from_year = int(from_date_parts[0]), from_date_parts[1], int(from_date_parts[2])
                        to_day, to_month, to_year = int(to_date_parts[0]), to_date_parts[1], int(to_date_parts[2])
                        from_date_obj = datetime.date(from_year, months.index(from_month) + 1, from_day)
                        to_date_obj = datetime.date(to_year, months.index(to_month) + 1, to_day)
                        delta = to_date_obj - from_date_obj
                        no_of_days = delta.days + 1 
                    else:
                        from_date = "Not Found"
                        to_date = "Not Found"
                        no_of_days = "Not Found"

                elif re.search(r"Composites penetration in Engineering Applications", extracted_text, re.I):
                    certificate_type = 'LECTURES Conducted'

                    if re.search(r'\b([A-Z]\.[A-Za-z]+)\b', extracted_text):
                        name = re.search(r'\b([A-Z]\.[A-Za-z]+)\b', extracted_text).group(1).strip()
                    else:
                        name = "Not Found"

                    if re.search(r'\bAssistant Professor\b', extracted_text):
                        designation = re.search(r'\bAssistant Professor\b', extracted_text).group(0).strip()
                    else:
                        designation = "Not Found"

                    if re.search(r'Department of ([A-Za-z\s]+)', extracted_text):
                        department = re.search(r'Department of ([A-Za-z\s]+)', extracted_text).group(1).strip()
                    else:
                        department = "Not Found"

                    if re.search( r'“([^”]+)”', extracted_text):
                        programme_conducted = re.search( r'“([^”]+)”', extracted_text).group(0)
                    else:
                        programme_conducted = "Not Found"

                    if re.search(r"([A-Za-z. ]+)(?:\s+Assistant Professor)?", extracted_text):
                        organizer = re.search(r"([A-Za-z. ]+)(?:\s+Assistant Professor)?", extracted_text).group(1).strip()
                    else:
                        organizer = "Not Found"

                    if re.search(r'Organized by (.*?) \d{1,2}-\d{1,2} [A-Za-z]+ \d{4}', extracted_text):
                        sponsor = re.search(r'Organized by (.*?) \d{1,2}-\d{1,2} [A-Za-z]+ \d{4}', extracted_text).group(1).strip()
                    else:
                        sponsor = "Not Found"

                    date_pattern = r'(\d{1,2} us [A-Za-z]+ \d{4})'

                    # Use regex to find the date in the extracted text
                    date_match = re.search(date_pattern, extracted_text)

                    if date_match:
                        date_str = date_match.group(1)
                        date_obj = datetime.strptime(date_str, '%d us %B %Y')
                        from_date = date_obj.strftime('%d %B %Y')
                        to_date = date_obj.strftime('%d %B %Y')
                        no_of_days = 1  # Since it's the same date, the duration is 1 day
                    else:
                        from_date = "Date not found"
                        to_date = "Date not found"
                        no_of_days = 0

                elif re.search(r'([A-Z]+)', extracted_text, re.I):
                    certificate_type = 'CONFERENCE Conducted' 
                    
                    if re.search( r'A Ba Dy(.*?)Me', extracted_text):
                        name = re.search( r'A Ba Dy(.*?)Me', extracted_text).group(0).strip()
                    else:
                        name = "Not Found"

                    if re.search(r"([A-Za-z\s]+Professor)", extracted_text):
                        designation = re.search(r"([A-Za-z\s]+Professor)", extracted_text).group(1).strip()
                    else:
                        designation = "Not Found"

                    if re.search(r'Faculty of [A-Z][a-zA-Z\s]+', extracted_text):
                        department = re.search(r'Faculty of [A-Z][a-zA-Z\s]+', extracted_text).group(1).strip()
                    else:
                        department = "Not Found"

                    if re.search(r'(\d+° [A-Za-z\s]+)', extracted_text):
                        programme_conducted = re.search(r'(\d+° [A-Za-z\s]+)', extracted_text).group(1).strip()
                    else:
                        programme_conducted = "Not Found"

                    date_pattern = r"(\w+) (\d+)-(\d+), (\d{4})"

                    # Use regex to find the date in the text
                    match = re.search(date_pattern, extracted_text)

                    if match:
                        month, start_day, end_day, year = match.groups()

                        # Define a mapping of month names to month numbers
                        month_mapping = {
                            'January': '01',
                            'February': '02',
                            'March': '03',
                            'April': '04',
                            'May': '05',
                            'June': '06',
                            'July': '07',
                            'August': '08',
                            'September': '09',
                            'October': '10',
                            'November': '11',
                            'December': '12',
                        }

                        # Create date strings
                        from_date = f"{year}-{month_mapping[month]}-{start_day}"
                        to_date = f"{year}-{month_mapping[month]}-{end_day}"

                        # Convert date strings to datetime objects
                        from_date = datetime.strptime(from_date, '%Y-%m-%d')
                        to_date = datetime.strptime(to_date, '%Y-%m-%d')

                        # Calculate the number of days
                        no_of_days = (to_date - from_date).days + 1
                    else:
                        from_date = "n"
                        to_date = "n"
                        no_of_days = "h"

                    if re.search(r'Organized by ([\w\s,]+)', extracted_text):
                        organizer = re.search(r'Organized by ([\w\s,]+)', extracted_text).group(2).strip()
                    else:
                        organizer = "Not Found"

                    if re.search(r'"(.*?)"', extracted_text):
                        sponsor = re.search(r'"(.*?)"', extracted_text).group(2).strip()
                    else:
                        sponsor = "Not Found"

                else:
                      certificate_type = "not found"

                # Continue with data insertion based on the certificate type
                if certificate_type == 'FDP Attended':
                    # Insert into FDP Attended table
                    fdp_attended_data = FDP_Attended(
                        name=name,
                        designation=designation,
                        department=department,
                        programme_attended=programme_attended,
                        from_date=from_date,
                        to_date=to_date,
                        organizer=organizer,
                        sponsor=sponsor,
                        no_of_days=no_of_days
                        # ... (Other fields)
                    )
                    db.session.add(fdp_attended_data)
                elif certificate_type == 'FDP Conducted':
                    # Insert into FDP Conducted table
                    fdp_conducted_data = FDP_Conducted(
                        name=name,
                        designation=designation,
                        department=department,
                        programme_conducted=programme_conducted,  # Set a default value
                        from_date=from_date,
                        to_date=to_date,
                        organizer=organizer,
                        sponsor=sponsor,
                        no_of_days=no_of_days
                        # ... (Other fields)
                    )
                    db.session.add(fdp_conducted_data)
                elif certificate_type == 'CONFERENCE Attended':
                    # Insert into CONFERENCE Attended table
                    conference_attended_data = CONFERENCE_Attended(
                        name=name,
                        designation=designation,
                        department=department,
                        programme_attended=programme_attended,
                        from_date=from_date,
                        to_date=to_date,
                        organizer=organizer,
                        sponsor=sponsor,
                        no_of_days=no_of_days
                        # ... (Other fields)
                    )
                    db.session.add(conference_attended_data)
                elif certificate_type == 'LECTURES Conducted':
                    # Insert into LECTURES Conducted table
                    lectures_conducted_data = LECTURES_Conducted(
                        name=name,
                        designation=designation,
                        department=department,
                        programme_conducted=programme_conducted,  
                        from_date=from_date,
                        to_date=to_date,
                        organizer=organizer,
                        sponsor=sponsor,
                        no_of_days=no_of_days
                        # ... (Other fields)
                    )
                    db.session.add(lectures_conducted_data)
                elif certificate_type == 'CONFERENCE Conducted':
                    # Insert into CONFERENCE Attended table
                    conference_conducted_data = CONFERENCE_Conducted(
                        name=name,
                        designation=designation,
                        department=department,
                        programme_conducted=programme_conducted,
                        from_date=from_date,
                        to_date=to_date,
                        organizer=organizer,
                        sponsor=sponsor,
                        no_of_days=no_of_days
                        # ... (Other fields)
                    )
                    db.session.add(conference_conducted_data)
                db.session.commit()

                os.remove(fdp_file_path)
                return render_template('fdp_result.html', extracted_text=extracted_text)
            else:
                os.remove(fdp_file_path)
                error_message = "Text extraction from the image failed. Please check the image quality."
                return render_template('fdp.html', error_message=error_message)

    # Handle the case where the form was not submitted correctly
    error_message = "File upload failed. Please select a valid file."
    return render_template('fdp.html', error_message=error_message)



@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if 'imageFile' not in request.files:
        return redirect(request.url)
    
    image_file = request.files['imageFile']
    if image_file.filename == '':
        return redirect(request.url)
    
    if image_file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        extracted_text = extract_text_from_image(image_path)
        os.remove(image_path)  # Remove the uploaded image after processing
        
        if extracted_text:
            return render_template('fdp_result.html', extracted_text=extracted_text)
        else:
            return "Text extraction failed."
    
    return "Upload failed."













# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'static\\uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER exists; if not, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/download_excel')
def download_excel():
    excel_file = "user_data.xlsx"
    return send_file(excel_file, as_attachment=True)
@app.route('/')
def index():
    return render_template('index.html')
# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        staffid = request.form['staffid']
        password = request.form['password']

        # Check if staffid is a 5-digit integer
        if staffid.isdigit() and len(staffid) == 5:
            # Query the database for the user
            user = User.query.filter_by(staffid=staffid).first()

            if user:
                if user.password == password:
                    session['staff_id'] = staffid  
                    session['name'] = user.name
                    session['email'] = user.email
                    session['contact_number'] = user.contact_number
                    session['designation'] = user.designation
                    session['company'] = user.company
                    session['user_role'] = user.user_role
                    # Create a new login history record when a user logs in
                    login_record = LoginHistory(user_id=user.id, staff_id=session['staff_id'], login_time=datetime.now())
                    db.session.add(login_record)
                    db.session.commit()            
                    
                    # Successful login
                    #return redirect('dashboard1.html')
                    return redirect('home1')
                
                else:
                    # Invalid password
                    return render_template('index.html', invalid_password="Invalid password!")
            else:
                # User not found, create a new user
                new_user = User(staffid=staffid, password=password)
                db.session.add(new_user)
                db.session.commit()
                return render_template('index.html', message="New user created!")
        else:
            # Invalid staff id
            return render_template('index.html', invalid_staffid="Invalid staff id!")



    return render_template('index.html')
@app.route('/home1',methods=['GET'])
def home1():
    staff_id = session.get('staff_id')

    user = User.query.filter_by(staffid=staff_id).first()
    staff_name = user.name if user else "Unknown Staff"  # Use a default name if the user is not found


    if user:
        session['name'] = user.name
        session['email'] = user.email
        session['contact_number'] = user.contact_number
        session['designation'] = user.designation
        session['company'] = user.company
    login_history = LoginHistory.query.order_by(LoginHistory.login_time.desc()).all()

 
    return render_template('home1.html', staff_id=staff_id,login_history=login_history, staff_name=staff_name,current_time=datetime.now())
   
@app.route('/fileupload', methods=['POST'])
def upload_file():
    message = ""  # Initialize the message variable
    invalid_password = ""  # Initialize the invalid_password variable
    
    staff_id = session.get('staff_id')
    
    if 'file' not in request.files:
        invalid_password = "No file part"
    else:
        file = request.files['file']
        if file.filename == '':
            invalid_password = "No selected file"
        else:
            # Generate a unique filename with staff ID, date, and time
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{current_time}_{secure_filename(file.filename)}"
            
            # Create a directory for the staff member if it doesn't exist
            staff_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(staff_id))
            os.makedirs(staff_folder, exist_ok=True)
            
            file_path = os.path.join(staff_folder, filename)
            file.save(file_path)
            message = "File uploaded successfully"
    
    return redirect(url_for('list_uploads')) 



@app.route('/list_uploads')
def list_uploads():
    staff_id = session.get('staff_id')
    
    if staff_id:
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(staff_id))
        
        # Check if the user has a folder, and list files from their folder
        if os.path.exists(user_folder):
            uploaded_files = os.listdir(user_folder)
        else:
            uploaded_files = []  # No files for this user
        
        return render_template('home1.html', staff_id=staff_id, uploaded_files=uploaded_files)
    
    # If the user is not logged in, you can redirect them to the login page or display an appropriate message.
    return redirect('/index')  # Redirect to the login page

    # Or display a message:
    # message = "Please log in to view your uploaded files."
    # return render_template('home1.html', message=message)

    
    # If the user is not logged in, you can redirect them to the login page or display an appropriate message.
    # Redirect example:
    # return redirect('/login')
    
    # Or display a message:
    # message = "Please log in to view your uploaded files."
    # return render_template('home1.html', message=message)






@app.route('/download/<staff_id>/<filename>')
def download_file(staff_id, filename):
    staff_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(staff_id))
    filepath = os.path.join(staff_folder, filename)

    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=False)
    else:
        invalid_password = "File not found. Please check the filename and try again."
    return render_template('home1.html', invalid_password=invalid_password)















@app.route('/view', methods=['GET', 'POST'])
def view_file():
    if request.method == 'POST':
        # Retrieve the filename from the form submission
        filename = request.form['filename']
    else:
        # Default to viewing the latest uploaded file
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
        if uploaded_files:
            filename = uploaded_files[-1]  # Get the last file in the list
        else:
            invalid_password= "No files uploaded yet."
        return render_template('home1.html', invalid_password=invalid_password)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists before attempting to serve it
    if os.path.exists(filepath):
        # Use Flask's send_file function to serve the file for viewing
        return send_file(filepath, as_attachment=False)
    else:
        invalid_password= "File not found. Please check the filename and try again."
    return render_template('home1.html',  invalid_password= invalid_password)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\DHAVASHRI\\Documents\\project\\static\\uploaded'

@app.route('/view-latest')
def view_latest_file():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    if not uploaded_files:
        # No files uploaded yet
        return render_template('home1.html', invalid_password="No files uploaded yet.")

    # Sort the list of files by modification time (newest first)
    uploaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)

    latest_file = uploaded_files[0]  # Get the first (latest) file in the sorted list
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)

    try:
        # Use Flask's send_file function to serve the file for viewing
        return send_file(filepath, as_attachment=False)
    except FileNotFoundError:
        # The file was not found
        return render_template('home1.html', invalid_password="File not found.")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return render_template('home1.html', invalid_password="An error occurred while trying to view the file.")



@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/dashboard1', methods=['GET', 'POST'])

def dashboard1():
    staff_id = session.get('staff_id')

    return render_template('dashboard1.html',staff_id=staff_id)
@app.route('/logout')
def logout():
    staff_id = session.pop('staff_id', None)
    user = User.query.filter_by(staffid=staff_id).first()

    if user:
        # Record logout history
        login_history = LoginHistory.query.filter_by(user_id=user.id, logout_time=None).order_by(LoginHistory.login_time.desc()).first()
        if login_history:
            login_history.logout_time = datetime.now()
            db.session.commit()

    return redirect(url_for('index'))








@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    show_modal = False
    
    if request.method == 'POST':
        staffid = request.form['staffid']
        user = User.query.filter_by(staffid=staffid).first()
        if user:
            # Generate a password reset token (for demonstration purposes)
            token = generate_random_token()

            # Save the token in the user's record (in a real application, use a more secure method like hashing)
            user.password_reset_token = token
            db.session.commit()

            # Send the password reset email
            send_password_reset_email(user)
            
            return render_template('index.html',email_success_message="An email has been sent to your registered email address with further instructions!")
        else:
            show_modal = True  
            return render_template('index.html',email_failed_message="User not found. Please enter a valid staff ID.",show_modal=show_modal)

    return render_template('index.html')
def generate_random_token():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(32))

def send_password_reset_email(user):
    # Generate the password reset link using the token
    reset_link = f" http://127.0.0.1:5000/reset-password/{user.password_reset_token}"
  


    # Create the email message
    subject = 'Password Reset Request'
    recipients = [user.email]
    message = f"Hi {user.staffid},\n\nPlease click the link below to reset your password:\n\n{reset_link}\n\nIf you didn't request this reset, please ignore this email."

    # Send the email
    msg = Message(subject=subject, recipients=recipients, body=message)
    mail.send(msg)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # Get the form inputs
        staffid = request.form['staffid']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Retrieve the user from the database
        user = User.query.filter_by(staffid=staffid).first()
        if user:
            if user.password == current_password:
                if new_password == confirm_password:
                    # Update the user's password
                    user.password = new_password
                    db.session.commit()
                
                
                    # Display a success message after password change
                    message = "Password changed successfully"
                    return render_template('change_password.html', message=message)
                else:
                    # New password and confirm password don't match
                    mismatch_message = "New password and confirm password do not match"
                    return render_template('change_password.html', mismatch_message=mismatch_message)
            else:
                # Invalid current password
                invalid_password = "Incorrect current password"
                return render_template('change_password.html', invalid_password=invalid_password)
        else:
            # User not found
            invalid_password = "User not found"
            return render_template('change_password.html', invalid_password=invalid_password)
    
    # Render the change password form
    return render_template('change_password.html',message=None)
# Import required libraries and modules

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Check if the token is valid and belongs to a user
    user = User.query.filter_by(password_reset_token=token).first()

    if not user:
        # If the token is not valid, redirect to an error page or display an error message
        flash('Invalid or expired token. Please request a new password reset link.')
        return redirect(url_for('forgot_password'))  # Replace 'forgot_password' with the appropriate route name for the forgot password page

    if request.method == 'POST':
        # Get the new password and confirm password from the form
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            # If passwords don't match, display an error message
            flash('Passwords do not match. Please try again.')
            return render_template('reset_password.html', token=token)

        # Update the user's password with the new one
        user.password = new_password
        user.password_reset_token = None  # Clear the password reset token
        db.session.commit()

        # Display a success message or redirect to a login page
        flash('Password changed successfully. You can now log in with your new password.')
        return redirect(url_for('login'))  # Replace 'login' with the appropriate route name for the login page

    # If it's a GET request, render the reset_password template with the token passed as an argument
    return render_template('reset_password.html', token=token)




@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # Assuming 'staff_id' is the user's identifier (staff ID) stored in the session
    staff_id = session.get('staff_id')

    # Retrieve the user's information from the database based on 'staff_id'
    user = User.query.filter_by(staffid=staff_id).first()

    if request.method == 'POST':
        # Update user information based on form data
        user.name = request.form['name']
        user.email = request.form['email']
        user.contact_number = request.form['contact_number']
        user.designation = request.form['designation']
        user.company = request.form['company']

        # Commit the changes to the database
        db.session.commit()

        flash('Profile updated successfully', 'success')

    return render_template('edit_profile.html', user=user)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        staff_id = session.get('staff_id')

        user = User.query.filter_by(staffid=staff_id).first()

        if user:
            # Check each form field and update if it's not empty
            if request.form['edit-name']:
                user.name = request.form['edit-name']
            if request.form['edit-email']:
                user.email = request.form['edit-email']
            if request.form['edit-contact']:
                user.contact_number = request.form['edit-contact']
            if request.form['edit-designation']:
                user.designation = request.form['edit-designation']
            if request.form['edit-company']:
                user.company = request.form['edit-company']

            # Commit the changes to the database
            db.session.commit()
            
            return render_template('home1.html', message1="Successfully updated")

        else:
            return render_template('home1.html', error="Error in update")
    except Exception as e:
        return render_template('profilepage.html', error=str(e))


    #except Exception as e:
        
        #return redirect(url_for('home1'))  # Redirect back to the profile page





@app.route('/dashboard')
def dashboard():
    uploaded_files = request.args.getlist('uploaded_files')
    return render_template('dashboard.html', uploaded_files=uploaded_files)









@app.route('/history')
def history():
    if 'user_role' in session and session['user_role'] == 'admin':
       login_history = LoginHistory.query.order_by(LoginHistory.login_time.desc()).all()
       return render_template('history.html', login_history=login_history)
       

    else:
      flash("You do not have permission to access this page.")
      return redirect(url_for('home1'))  # Redirect to home1 page with a flash message












@app.route('/admin-view-files', methods=['GET', 'POST'])
def admin_view_files():
    if 'user_role' in session and session['user_role'] == 'admin':
        staff_id = request.form.get('staff_id')

        if staff_id:
            staff_folder = os.path.join(app.config['UPLOAD_FOLDER'], staff_id)
            if os.path.exists(staff_folder):
                uploaded_files = os.listdir(staff_folder)
            else:
                uploaded_files = []
        else:
            uploaded_files = []

        return render_template('home1.html', staff_id=staff_id, uploaded_files=uploaded_files)
    else:
        flash("You don't have permission to view this content.")
        return redirect(url_for('home1'))


















#jupy try
@app.route('/runjupyter', methods=['GET', 'POST'])
def runjupyter():
    # Execute the Jupyter Notebook code using subprocess
    try:
        subprocess.run(['jupyter', 'nbconvert', '--execute', 'Certificate Text Extraction Project - All in one - 04-06-2023 (1).ipynb'])
        output = "Jupyter Notebook executed successfully."
    except Exception as e:
        output = f"Error executing Jupyter Notebook: {str(e)}"

    # Render a template to display the output
    return render_template('output.html', output=output)


@app.route('/search', methods=['GET'])
def search():
    # Get the user-provided keyword from the query parameter
    keyword = request.args.get('city')

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    name =  request.args.get('name')
    print(f"Date:{start_date}")
    # Convert the string to a datetime object
    if start_date:
       date_object1 = datetime.strptime(start_date, '%Y-%m-%d')
       formatted_date1 = date_object1.strftime('%d-%m-%Y')
    if end_date:
       date_object2 = datetime.strptime(end_date, '%Y-%m-%d')
       formatted_date2 = date_object2.strftime('%d-%m-%Y')


# Format the datetime object to the desired format dd-mm-yyyy
    
   


# Print the formatted date
   # print(f" Formatted Date1:{formatted_date1}")
    #Sprint(f" Formatted Date2:{formatted_date2}")

    # Check if a keyword was provided
    if not keyword:
        return render_template('home1.html', message="Please enter a keyword")

    # Remove spaces and underscores from the keyword and convert it to lowercase
    cleaned_keyword = keyword.replace(" ", "").replace("_", "").lower()

    # Print the cleaned keyword for debugging
    print(f"Cleaned Keyword: {cleaned_keyword}")

    # Construct a list of all table names in the database
    dbpath = 'C:/Users/DHAVASHRI/Documents/project/instance/login.db'
    connection = sqlite3.connect(dbpath)
    cursor = connection.cursor()
    
    # Get a list of all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    table_names = [name[0] for name in table_names]

    # Close the database connection
    connection.close()

    # Print the list of table names for debugging
    print(f"Table Names: {table_names}")
  

    # Search for a table that contains the cleaned_keyword (case-insensitive)
    matching_tables = [table for table in table_names if cleaned_keyword in table.replace(" ", "").replace("_", "").lower()]

    # Print the matching tables for debugging
    print(f"Matching Tables: {matching_tables}")

    if not matching_tables:
        return render_template('home1.html', message=f"No tables matching the keyword '{keyword}'")

    # Use the first matching table (you can handle multiple matches differently if needed)
    selected_table = matching_tables[0]

    # Construct the SQL query to select all data from the selected table
    if name and start_date and end_date:
        sql_query = f"SELECT * FROM {selected_table} WHERE from_date = '{formatted_date1}' AND to_date = '{formatted_date2}' AND name LIKE '%{name}%' "
    if name:
        sql_query = f"SELECT * FROM {selected_table} WHERE name LIKE '%{name}%'"

    if start_date and end_date:
       sql_query = f"SELECT * FROM {selected_table} WHERE from_date = '{formatted_date1}' AND to_date = '{formatted_date2}'"
    
    sql_query=f"SELECT * FROM {selected_table}"

    # Connect to the database again
    connection = sqlite3.connect(dbpath)
    cursor = connection.cursor()

    try:
        # Execute the SQL query
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Extract the specific columns from each row
        results = [(row[0], row[1], row[2], row[3],row[4],row[9]) for row in rows]

    except sqlite3.OperationalError as e:
        print(f"Error: {e}")  # Print any database-related errors for debugging
        return render_template('home1.html', message=f"Failed to retrieve data from table '{selected_table}'")

    # Close the database connection
    connection.close()
    session['results'] = results

    return render_template('home1.html', results=results)














@app.route('/export_csv', methods=['POST'])
def export_csv():
    if request.method == 'POST':
        # Implement your logic to get filtered_data based on the search query or other criteria
        if 'results' in session:
            results = session['results']
        filtered_data = results  # Replace with your filtered data

        # Prepare a CSV response
        output_csv = io.StringIO()
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(['ID', 'Name', 'Designation', 'Department', 'Program Name','No.of Days'])  # Write the header row
        csv_writer.writerows(filtered_data)  # Write the data rows
        output_csv.seek(0)  # Move the file pointer to the beginning

        # Send the CSV file as a response
        return Response(
            output_csv,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=exported_data.csv'}
        )
#sample

if __name__ == '__main__':
    
    app.run(debug=True)




































  





    
























