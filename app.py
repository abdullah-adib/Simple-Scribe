import os
from dotenv import load_dotenv
from distutils.log import debug
from flask import Flask, render_template
app = Flask(__name__)

# load_dotenv()
# globals.prefix = os.environ.get('PREFIX')
# globals.token = os.environ.get('BOT_TOKEN')
# globals.eventToken = os.environ.get('TICKETMASTER_TOKEN')
# globals.apireq = EventRequester()

@app.route('/')
@app.route('/home')

def home_page():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)
