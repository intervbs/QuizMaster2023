from wtforms import Form, StringField, validators, PasswordField
from wtforms.validators import Email, InputRequired, EqualTo
from email_validator import validate_email, EmailNotValidError

class Reg_user(Form):
    '''Form for registrating a new user'''
    username = StringField('Username', [validators.Length(min = 3, max = 55)], render_kw={'placeholder': 'Enter your username'})
    firstname = StringField('First Name', [validators.Length(min = 1, max = 55)], render_kw={'placeholder': 'Enter your First Name'})
    lastname = StringField('Last Name', [validators.Length(min = 2, max = 55)], render_kw={'placeholder': 'Enter your Last Name'})
    email = StringField('Email', validators=[validators.Length(min = 3, max = 150), Email(message='Please input a valid email')], render_kw={'placeholder': 'Enter your Email'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 150), EqualTo('confirm')], render_kw={'placeholder': 'Enter your password'})
    confirm = PasswordField('Repete Password', render_kw={'placeholder': 'Confirm your password'})

