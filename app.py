import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from peewee import *
from lib.account import *
from datetime import timedelta
from lib.listing import *
from lib.availability import *
import json

# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a7sk21'
app.permanent_session_lifetime = timedelta(minutes=120)

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
    listings = Listing.select()
    return render_template('index.html', account=session.get('username'), listings=listings)

@app.route('/signup', methods=['GET'])
def get_signup():
    if session.get('username') != None:
        return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def post_signup():
    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['firstname']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    # We eventually some checks before creating a new user e.g. that email is unique, email is in valid format etc.
    account = Account(username=username, first_name=firstname, last_name=lastname, email=email, phone_number=phone, password=password)
    account.save()

    session.permanent = True
    session['username'] = account.username
    return redirect(f"/")

@app.route('/login', methods=['GET'])
def get_login():
    if session.get('username') != None:
        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    email = request.form['email']
    password = request.form['password']
    try:
        accounts = Account.select().where(Account.email == email)
        if accounts.exists(): 
            if password == accounts[0].password:
                account = accounts[0]
                session.permanent = True
                session['username'] = account.username
                return redirect('/')
            else:
                error_message = "Incorrect password. Please try again."
        else:
            error_message = "User not found. Please check your email."
    except Account.DoesNotExist:
        error_message = "An error occurred during login. Please try again."

    # Pass the error message to the template and render the login page
    return render_template('login.html', error=error_message)

@app.route('/logout', methods=['GET'])
def logout():
    # Clear the user_id from the session
    session.pop('username', None)
    return redirect('/')

@app.route('/add-space', methods=['GET'])
def add_space():
    if session.get('username') == None:
        return redirect('/login')
    return render_template('add_listing.html', account=session.get('username'))

@app.route('/', methods=['POST'])
def post_listing():
    if session.get('username') == None:
        return redirect('/login')
    else:
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        price = request.form['price']

        person = Account.get(Account.username==session.get('username'))
        listing = Listing(name=name, address=address, description=description, price=price, account=person)
        listing.save()
        listings = Listing.select()
        return redirect(f"/listings/{listing.id}")

@app.route('/listings/<int:id>', methods=['GET'])
def get_listing(id):
    individual_listing = Listing.get(Listing.id == id)
    # print("individual listing: ", individual_listing)
    
    # Fetch the availabilities for the listing
    availabilities = Availability.select().where(Availability.listing_id == individual_listing.id)
    print("availability.listing_id: ", availabilities[0].listing_id)
    # Create a list to hold the availability data as dictionaries
    availability_data = []
    for availability in availabilities:
        if availability.available == True:
            availability_data.append({
                'title': 'Available',
                'start': availability.start_date.isoformat(),  # Convert to ISO format
                'end': availability.end_date.isoformat(),      # Convert to ISO format
            })
    
    # # Convert the list to a JSON object
    availability_json = json.dumps(availability_data)
    return render_template('show.html', listing=individual_listing, account=session.get('username'), availability_json=availability_json)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))


    
