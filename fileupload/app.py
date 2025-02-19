from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'static/uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER exists; if not, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('fdp.html')

@app.route('/fileupload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        # Save the uploaded file to the specified folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return "File uploaded successfully"

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
            return "No files uploaded yet."

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists before attempting to serve it
    if os.path.exists(filepath):
        # Use Flask's send_file function to serve the file for viewing
        return send_file(filepath, as_attachment=False)
    else:
        return "File not found. Please check the filename and try again."
@app.route('/view-latest')
def view_latest_file():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if uploaded_files:
        # Sort the list of files by modification time (newest first)
        uploaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
        latest_file = uploaded_files[0]  # Get the first (latest) file in the sorted list
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)
        return send_file(filepath, as_attachment=False)
    else:
        return "No files uploaded yet."


if __name__ == '__main__':
    app.run(debug=True)
