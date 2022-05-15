import os
import threading
# import asyncio
import uuid
from os.path import exists
import base64
from dotenv import load_dotenv
from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, abort, make_response
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_wtf.file import FileField
from wtforms import SubmitField
import assemblyai
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

user_id_key = "user_id"

def getCookie():
    if not request.cookies.get('uid'):
        res = make_response("Setting a cookie")
        cookieValue = uuid.uuid4().hex
        res.set_cookie('uid', cookieValue, max_age=3600)
    else:
        cookieValue = request.cookies.get('uid')
        res = make_response("Value of cookie foo is {}".format(cookieValue))
    return (res, cookieValue)

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

# delete file
@app.route('/delete_file', methods=['POST'])
def delete_file():
    print('delete request')
    filename = secure_filename(request.form['name'])
    if filename == '':
        return "No file submitted.", 400
    resp, actualFilename = getCookie()
    path = os.path.join(app.config['UPLOAD_PATH'], actualFilename)
    if not exists(path):
        return "File does not exist.", 400
    print('deleting ' + filename)
    os.remove(path)
    return resp

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
    resp, actualFilename = getCookie()
    uploaded.save(os.path.join(app.config['UPLOAD_PATH'], actualFilename))
    return resp

# LOCK FILE
def getLockFilePath(uid):
    return os.path.join(app.config['UPLOAD_PATH'], \
        secure_filename('{}.LOCK'.format(uid)))

def createLockFile(uid):
    if not checkForLockFile(uid):
        with open(getLockFilePath(uid), 'w') as fp:
            pass

# true -> lock exists
def checkForLockFile(uid):
    return exists(getLockFilePath(uid))

def removeLockFile(uid):
    if checkForLockFile(uid):
        os.remove(getLockFilePath(uid))

# RESULT FILE
def getResultFilePath(uid):
    return os.path.join(app.config['UPLOAD_PATH'], \
        secure_filename('{}.RESULT'.format(uid)))

# true -> result exists
def checkForResultFile(uid):
    return exists(getResultFilePath(uid))

def createResultFile(uid, text):
    # if not checkForLockFile(uid):
    with open(getResultFilePath(uid), 'w') as fp:
        fp.write(text)

def removeResultFile(uid):
    if checkForResultFile(uid):
        os.remove(getResultFilePath(uid))

def readResultFile(uid):
    rf = open(getResultFilePath(uid), "r")
    return rf.read()

# TRANSCRIBE WORKERS
def createNewTranscribeTask(uid):
    print('{}: creating new worker'.format(uid))
    createLockFile(uid)
    path = os.path.join(app.config['UPLOAD_PATH'], uid)
    text = assemblyai.getTranscript(path)
    createResultFile(uid, text)
    print('{}: worker finished'.format(uid))

# returns None when the worker is not done yet
def getTranscribeResult(uid):
    if not checkForResultFile(uid):
        return None
    # transcribe worker is done, return the result
    text = readResultFile(uid)
    removeResultFile(uid)
    removeLockFile(uid)
    return text

@app.route('/start_transcribe', methods=['POST'])
def start_transcribe():
    print('got transcribe start request')
    resp, uid = getCookie()
    path = os.path.join(app.config['UPLOAD_PATH'], uid)
    # check if there is already an active worker
    if checkForLockFile(uid):
        print('transcribe worker already running')
        return resp
    # create new worker
    threading.Thread(target=createNewTranscribeTask, args=(uid,)).start()
    # tmp.append(asyncio.create_task(createNewTranscribeTask(uid)))
    # asyncio.to_thread(createNewTranscribeTask, uid)
    return resp

@app.route('/transcribe_ping', methods=['GET'])
def transcribe_ping():
    print('got transcribe ping request')
    resp, uid = getCookie()
    path = os.path.join(app.config['UPLOAD_PATH'], uid)
    result = getTranscribeResult(uid)
    if not (result is None):
        print("worker finished with result: " + result)
    return '' if result is None else result 

if __name__ == "__main__":
    app.run(debug=True)
