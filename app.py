import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from peewee import *
from lib.account import *


# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a7sk21'

# Environment variables
load_dotenv()
db_username = os.getenv('DB_USERNAME')
print(db_username)

# Create new database instance
db = PostgresqlDatabase(
    'makersbnb-red-team',  # Your database name
    user=db_username,  # Your PostgreSQL username
    password='',  # Your PostgreSQL password
    host='localhost'  # Your PostgreSQL host
)

# Initialize the database connection in the Flask app context
@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

# == Your Routes Here ==

# GET /
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

def is_logged_in():
    return 'user_id' in session

@app.route('/login', methods=['POST'])
def post_login():
    email = request.form['email']
    password = request.form['password']
    try:
        accounts = Account.select().where(Account.email == email)
        if accounts.exists():  # Check if any matching accounts were found
            if password == accounts[0].password:
                account = accounts[0]
                session['username'] = account.username
                person = session.get('username')
                return render_template('index.html', account=person)
            else:
                error_message = "Incorrect password. Please try again."
        else:
            error_message = "User not found. Please check your email."
    except Account.DoesNotExist:
        error_message = "An error occurred during login. Please try again."

    # Pass the error message to the template and render the login page
    return render_template('login.html', error=error_message)

@app.route('/<int:id>', methods=['GET'])
def get_account_page():
    if not is_logged_in():
        return redirect('/login')
    else:
        logged_in_user = is_logged_in()
        return render_template('login.html', account=logged_in_user)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Clear the user_id from the session
    return redirect('/')

@app.route('/profile', methods=['GET'])
def get_profile():
    if not is_logged_in():
        return redirect('/login')
    # Continue with displaying the user's profile

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))