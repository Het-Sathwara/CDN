from flask import Flask, jsonify, request, send_from_directory
import sys
import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # Add this line
port = int(sys.argv[1])
UPLOAD_FOLDER = f'uploads_{port}'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

# Create upload directory if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def serve_content():
    return f'''
    <html>
        <body>
            <h1>Server on Port {port}</h1>
            <p>This content is served from backend server running on port {port}</p>
            <h3>Upload File</h3>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
            <h3>Uploaded Files:</h3>
            {''.join(f'<p><a href="/files/{f}">{f}</a></p>' for f in os.listdir(UPLOAD_FOLDER))}
        </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File uploaded to port {port}: <a href="/files/{filename}">{filename}</a>'
    return 'Invalid file type', 400

@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health_check():
    return jsonify(status="healthy", port=port)

if __name__ == '__main__':
    app.run(port=port)