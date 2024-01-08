import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from peewee import *

# Create a new Flask app
app = Flask(__name__)

# Environment variables
load_dotenv()
db_username = os.getenv('DB_USERNAME')
print(db_username)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
