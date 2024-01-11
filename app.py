import os
from flask import Flask, request, render_template, redirect, session, url_for
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from peewee import *
from lib.account import *
from datetime import timedelta
from lib.listing import *
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators, IntegerField
from wtforms.validators import Regexp, ValidationError, InputRequired, Email
from sqlalchemy.exc import IntegrityError
from lib.availability import *
import json
from flask_bcrypt import Bcrypt


# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a7sk21'
bcrypt = Bcrypt(app)
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

class SignupForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    firstname = StringField('First Name', [InputRequired()])
    lastname = StringField('Last Name', [InputRequired(message='Last name cannot be blank.')])
    email = StringField('Email', [InputRequired(), Email(message='Invalid email address.')])
    phone = StringField('Phone', [InputRequired(), Regexp(r'^\d{11}$', message='Phone number must be 11 digits')])
    password = PasswordField('Password', [InputRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField("Login")

class AddListingForm(FlaskForm):
    name = StringField('Name', [InputRequired()])
    address = StringField('Address', [InputRequired()])
    description = StringField('Description', [InputRequired()])
    price = StringField('Price', [InputRequired()]) 
    submit = SubmitField("Add Space")

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
    form = SignupForm()
    if form.validate_on_submit():
        # Form is valid, proceed with creating the account
        username = form.username.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password)

        try:
            account = Account.create(
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=email,
                phone_number=phone,
                password=hashed_password
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


# @app.route('/login', methods=['GET'])
# def get_login():
#     if session.get('username') != None:
#         return redirect('/')
#     else:
#         return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message=None
    if form.validate_on_submit():
        print(form.errors)
        try:
            account = Account.select().where(Account.email == form.email.data).first()
            if account: 
                if account.password == form.password.data or bcrypt.check_password_hash(account.password, form.password.data):
                    account = account
                    session.permanent = True
                    session['username'] = account.username
                    return redirect('/')
                else:
                    error_message = "Incorrect password. Please try again."
            else:
                error_message = "User not found. Please try again."
        except Account.DoesNotExist:
            error_message = "An error occurred during login. Please try again."
    else:
        if session.get('username') != None:
            return redirect('/')
    return render_template('login.html', form=form, error_message=error_message)

@app.route('/logout', methods=['GET'])
def logout():
    # Clear the user_id from the session
    session.pop('username', None)
    return redirect('/')

@app.route('/add-space', methods=['GET', 'POST'])
def add_space():
    form = AddListingForm()
    if session.get('username') == None:
        return redirect('/login')
    else:
        if form.validate_on_submit():
            name = form.name.data
            address = form.address.data
            description = form.description.data
            price = form.price.data

            person = Account.get(Account.username==session.get('username'))
            listing = Listing(name=name, address=address, description=description, price=price, account=person)
            listing.save()
            return redirect(f"/listings/{listing.id}")
    return render_template('add_listing.html', account=session.get('username'), form=form)


@app.route('/listings/<int:id>', methods=['GET', 'POST'])
def get_listing(id):
    individual_listing = Listing.get(Listing.id == id)
    
    availabilities = Availability.select().where(Availability.listing_id == individual_listing.id)
    
    if session.get('username') != None:
        logged_in_user = Account.get(Account.username == session.get('username'))
        print(logged_in_user)
        
        if request.method == 'POST':
            start_date = request.form['start-date']
            end_date = request.form['end-date']
            if logged_in_user.id == individual_listing.account_id:

                new_availability = Availability.create(
                    listing_id=individual_listing,
                    start_date=start_date,
                    end_date = end_date,
                    available=True
                )
                new_availability.save()

            return redirect(url_for('get_listing', id=id))

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
    return render_template('show.html', listing=individual_listing, logged_in_user=logged_in_user, account=session.get('username'), availability_json=availability_json)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))


    
