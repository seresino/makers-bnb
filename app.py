import os
from flask import Flask, request, render_template, redirect, session, url_for, flash
from lib.database_connection import get_flask_database_connection
from dotenv import load_dotenv
from peewee import *
from lib.account import *
from datetime import timedelta
from lib.listing import *
from peewee import IntegrityError
from lib.availability import *
import json
from flask_bcrypt import Bcrypt
from lib.booking import *
from datetime import datetime
from utils import *
from forms import *
from twilio.rest import Client

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
            account.save()

            session.permanent = True
            session['username'] = account.username

            # Redirect to the home page after successful signup
            return redirect(url_for('get_index'))

        except IntegrityError:
            # Handle the case where a unique constraint (username or email) is violated
            flash("username or email already exists.", 'error')
            return render_template('signup.html', form=form)

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
    logged_in_user=False

    individual_listing = Listing.get(Listing.id == id)
    listing_owner = Account.get(Account.id == individual_listing.account_id)
    
    availabilities = Availability.select().where(Availability.listing_id == individual_listing.id)
    availability_data = []
    for availability in availabilities:
        if availability.available == True:
            availability_data.append({
                'title': 'Available',
                'start': availability.start_date.isoformat(),  # Convert to ISO format
                'end': availability.end_date.isoformat(),      # Convert to ISO format
            })
    
    # Convert the list to a JSON object
    availability_json = json.dumps(availability_data)
    
    if session.get('username') != None:
        logged_in_user = Account.get(Account.username == session.get('username'))
        
        if request.method == 'POST':
            start_date = request.form['start-date']
            end_date = request.form['end-date']
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if logged_in_user.id == individual_listing.account_id:

                if not check_availability_overlap(availabilities, start_date, end_date):
                    new_availability = Availability.create(
                    listing_id=individual_listing,
                    start_date=start_date,
                    end_date = end_date,
                    available=True
                )

                    new_availability.save()
                    flash("Availability updated", 'sucess')
        
                else:
                    flash("Overlaps with existing availability", 'error')


            else:
                if check_requested_booking_availability(availabilities, start_date, end_date):

                    new_booking_request = Booking.create(
                        listing_id = individual_listing,
                        account_id = logged_in_user,
                        start_date = start_date,
                        end_date = end_date,
                        status = 'Requested'
                    )
                    new_booking_request.save()
                    flash("Booking requested", 'success')
                    
                    message = f"Hello {listing_owner.first_name}, Your property {individual_listing.name} has been requested from {start_date} to {end_date}. Please login to your account to manage this request. Thanks MakersBnB"
                    send_request_sms(os.getenv('TWILIO_PHONE_NUMBER'), '447590395227', message)
                else:
                    flash("Property not avilable for given dates", 'error')

            return redirect(url_for('get_listing', id=id))
    
    return render_template('show.html', listing=individual_listing, logged_in_user = logged_in_user, account=session.get('username'), availability_json=availability_json)

        # # Check if there are pending booking requests for this listing
        # pending_requests = Booking.select().where(
        #     (Booking.listing_id == individual_listing.id) &
        #     (Booking.status == 'Requested')
        # )

        # return render_template('show.html', listing=individual_listing, logged_in_user=logged_in_user,
        #                     account=session.get('username'), availabilities=availabilities,
        #                     pending_requests=pending_requests)




@app.route('/listings/<int:listing_id>/bookings/<int:booking_id>', methods=['POST'])
def handle_booking_action(listing_id, booking_id):
    if session.get('username') is None:
        return redirect('/login')

    logged_in_user = Account.get(Account.username == session.get('username'))
    listing = Listing.get(Listing.id == listing_id)

    # Ensure the logged-in user is the owner of the listing
    if logged_in_user.id != listing.account_id:
        return redirect(url_for('get_listing', id=listing_id))

    booking = Booking.get(Booking.id == booking_id)
    booking_user = Account.get(Account.id == booking.account_id)

    # Update the status of the booking based on the action
    action = request.form.get('action')

    if action == 'accept':
        booking.status = 'Confirmed'
        remove_availability(booking)
    elif action == 'deny':
        booking.status = 'Denied'
    message = f"Hello {booking_user.first_name}, your request for {listing.name} has been {booking.status}. Please login to your account for further details. Thanks MakersBnB"
    send_request_outcome_sms(os.getenv('TWILIO_PHONE_NUMBER'), '447590395227', message)
    booking.save()

    return redirect(url_for('get_listing', id=listing_id))



@app.route('/bookings', methods=['GET'])
def get_bookings():
    if session.get('username') == None:
        return redirect('/login')
    else:
        person = Account.get(Account.username==session.get('username'))
        listings = Listing.select().where(Listing.account_id==person.id)

        received = Booking.select().where(Booking.listing_id << [listing.id for listing in listings])
        received_names = {booking.listing_id: listing.name for booking, listing in zip(received, listings)}

        requested = Booking.select().where(Booking.account_id == person.id)
        other_listings = []
        for booking in requested:
            other_listings.append(Listing.get(Listing.id == booking.listing_id))
        requested_names = {booking.listing_id: listing.name for booking, listing in zip(requested, other_listings)}

        return render_template('bookings.html', account=session.get('username'), received=received, received_names=received_names, requested=requested, requested_names=requested_names)

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))


    
