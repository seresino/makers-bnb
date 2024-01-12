from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators, IntegerField, FileField
from wtforms.validators import Regexp, ValidationError, InputRequired, Email

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
    price = IntegerField('Price', [InputRequired()]) 
    image = FileField('Image') 
    submit = SubmitField("Add Space")
