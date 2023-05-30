from flask import Flask, render_template, request
import os
import datetime
import pytesseract
from PIL import Image
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route to handle form submission
@app.route('/success', methods=['POST'])
def upload():
    # Get the uploaded file from the form
    uploaded_file = request.files['file']

    # Save the uploaded file to a directory
    file_path = uploaded_file.filename
    uploaded_file.save(file_path)

    # Get the date and time for text extraction
    extraction_datetime_str = request.form['datetime']
    extraction_datetime = datetime.strptime(extraction_datetime_str, '%Y-%m-%dT%H:%M')


    # Schedule the text extraction
    scheduler.add_job(extract_text, 'date', run_date=extraction_datetime, args=[file_path])
    text1=extract_text(file_path)
    return render_template("result_data.html", result=text1)

# Function to extract text from the TIFF image using OCR
def extract_text(file_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)
