import os
from dotenv import load_dotenv
from distutils.log import debug
from flask import Flask
app = Flask(__name__)

# load_dotenv()
# globals.prefix = os.environ.get('PREFIX')
# globals.token = os.environ.get('BOT_TOKEN')
# globals.eventToken = os.environ.get('TICKETMASTER_TOKEN')
# globals.apireq = EventRequester()

@app.route('/')
def hello_world():
    return 'Hello, World!!!'

if __name__ == "__main__":
    app.run(debug=True)
