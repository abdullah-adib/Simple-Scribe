import os
from dotenv import load_dotenv
from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, abort

from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

import globals

class AudioForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')

app = Flask(__name__, template_folder='templates',static_folder='css')

# limit max upload size to 8 MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8

# restrict file extensions
app.config['UPLOAD_EXTENSIONS'] = [
    '.3ga', '.aac', '.ac3', '.aif', '.aiff', '.alac', '.amr', '.ape', '.au', 
    '.dss', '.flac', '.flv', '.m4a', '.m4b', '.m4p', '.mp3', '.mpga', '.ogg,',
    '.oga,', '.mogg', '.opus', '.qcp', '.tta', '.voc', '.wav', '.wma', '.wv',
    '.webm', '.MTS,', '.M2TS,', '.TS', '.mov', '.mp4,', '.m4p,', '.m4v', '.mxf'
]

# set global state
# load environment variables from .env
load_dotenv()
globals.ASSEMBLYAI_API_KEY = os.environ.get('ASSEMBLYAI_API_KEY')

@app.route('/')
@app.route('/home')

def home_page():
    return render_template('base.html')

# file upload event 
@app.route('/', methods=['POST'])
def upload_file():
    print('got upload request')
    uploaded = request.files['file']
    filename = secure_filename(uploaded.filename)
    if filename == '':
        abort(400)
    ext = os.path.splitext(uploaded.filename)[1]
    if ext not in app.config['UPLOAD_EXTENSIONS']:
        abort(400)
    print('accepted file:' + filename)
    return redirect(url_for('/home'))


if __name__ == "__main__":
    app.run(debug=True)
