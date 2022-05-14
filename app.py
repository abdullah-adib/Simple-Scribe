import os
import requests
from dotenv import load_dotenv
from distutils.log import debug
from flask import Flask, render_template
import globals
app = Flask(__name__, template_folder='templates',static_folder='css')


# set global state
# load environment variables from .env
load_dotenv()
globals.ASSEMBLYAI_API_KEY = os.environ.get('ASSEMBLYAI_API_KEY')

@app.route('/')
@app.route('/home')

def home_page():
    return render_template('base.html')

def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
