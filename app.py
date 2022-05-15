import os
from os.path import exists
import base64
from dotenv import load_dotenv
from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, abort

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_wtf.file import FileField
from wtforms import SubmitField

import globals

class AudioForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')

# app configuration
app = Flask(__name__, template_folder='templates',static_folder='css')

maxSize = 8

# limit max upload size to 8 MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * maxSize

# uploads path
app.config['UPLOAD_PATH'] = 'uploads'

# restrict file extensions
app.config['UPLOAD_EXTENSIONS'] = [
    '.3ga', '.aac', '.ac3', '.aif', '.aiff', '.alac', '.amr', '.ape', '.au', 
    '.dss', '.flac', '.flv', '.m4a', '.m4b', '.m4p', '.mp3', '.mpga', '.ogg,',
    '.oga,', '.mogg', '.opus', '.qcp', '.tta', '.voc', '.wav', '.wma', '.wv',
    '.webm', '.MTS,', '.M2TS,', '.TS', '.mov', '.mp4,', '.m4p,', '.m4v', '.mxf'
]

# csrf protection
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key
app.config['DROPZONE_ENABLE_CSRF'] = True
csrf = CSRFProtect(app)

# set global state
# load environment variables from .env
load_dotenv()
globals.ASSEMBLYAI_API_KEY = os.environ.get('ASSEMBLYAI_API_KEY')

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('base.html')

@app.errorhandler(CSRFError)
def csrf_error(e):
    return e.description, 400

@app.errorhandler(413)
def too_large(e):
    print('rejected file:' + filename)
    return "File too large (max {}MB)".format(maxSize), 413

@app.route('/delete_file', methods=['POST'])
def delete_file():
    print('delete request')
    filename = secure_filename(request.form['name'])
    if filename == '':
        return "No file submitted.", 400
    path = os.path.join(app.config['UPLOAD_PATH'], filename)
    if not exists(path):
        return "File does not exist.", 400
    print('deleting ' + filename)
    os.remove(path)
    return '', 204

# file upload event 
@app.route('/upload_file', methods=['POST'])
def upload_file():
    print('got upload request')
    uploaded = request.files['file']
    filename = secure_filename(uploaded.filename)
    if filename == '':
        return "No file submitted.", 400
    ext = os.path.splitext(uploaded.filename)[1]
    if ext not in app.config['UPLOAD_EXTENSIONS']:
        print('rejected file:' + filename)
        return "Bad file extension.", 400
    print('accepted file:' + filename)
    uploaded.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
