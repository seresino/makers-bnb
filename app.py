import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from peewee import *
from lib.account import *
from datetime import timedelta
from lib.listing import *
from wtforms import Form, StringField, validators
from wtforms.validators import Regexp, ValidationError
from sqlalchemy.exc import IntegrityError

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


class SignupForm(Form):
    username = StringField('Username', [validators.InputRequired(message='Username cannot be blank.')])
    firstname = StringField('First Name', [validators.InputRequired(message='First Name cannot be blank.')])
    lastname = StringField('Last Name', [validators.InputRequired(message='Last name cannot be blank.')])
    email = StringField('Email', [validators.InputRequired(message='Email is required.'), validators.Email(message='Invalid email address.')])
    phone = StringField('Phone', [validators.InputRequired(message='Phone number is required'), Regexp(r'^\d{10}$', message='Phone number must be 10 digits')])
    password = StringField('Password', [validators.InputRequired(message='Password cannot be blank.')])

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
        form = SignupForm()
        error = None
        return render_template('signup.html', form=form, error=error)


@app.route('/signup', methods=['POST'])
def post_signup():
    form = SignupForm(request.form)
    if form.validate():
        # Form is valid, proceed with creating the account
        username = form.username.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data

        try:
            account = Account.create(
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=email,
                phone_number=phone,
                password=password
            )

            session.permanent = True
            session['username'] = account.username

            # Redirect to the home page after successful signup
            return redirect(url_for('get_index'))

        except IntegrityError:
            # Handle the case where a unique constraint (username or email) is violated
            error = 'Username or email already exists'
            return render_template('signup.html', form=form, error=error)

    else:
        # Form is not valid, render the signup page with errors
        return render_template('signup.html', form=form)


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
    listing = Listing.get(Listing.id == id)
    return render_template('show.html', listing=listing, account=session.get('username'))


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))


    
