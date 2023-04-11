from wtforms import Form, StringField, validators, PasswordField, EmailField, TextAreaField, SubmitField, BooleanField, HiddenField
from wtforms.validators import Email, InputRequired, EqualTo, DataRequired
from email_validator import validate_email, EmailNotValidError

class Login_user(Form):
    '''Form for login page'''
    username = StringField('Username', [validators.Length(min = 3, max = 55)], render_kw={'placeholder': 'Enter your username'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 150)], render_kw={'placeholder': 'Enter your password'})

class Reg_user(Form):
    '''Form for registrating a new user'''
    username = StringField('Username', [validators.Length(min = 3, max = 55)], render_kw={'placeholder': 'Enter your username'})
    firstname = StringField('First Name', [validators.Length(min = 1, max = 55)], render_kw={'placeholder': 'Enter your First Name'})
    lastname = StringField('Last Name', [validators.Length(min = 2, max = 55)], render_kw={'placeholder': 'Enter your Last Name'})
    email = EmailField('Email', validators=[validators.Length(min = 3, max = 150), Email(message='Please input a valid email')], render_kw={'placeholder': 'Enter your Email'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 150), EqualTo('confirm')], render_kw={'placeholder': 'Enter your password'})
    confirm = PasswordField('Repete Password', render_kw={'placeholder': 'Confirm your password'})

class New_quiz(Form):
    '''Form for making a new quiz'''
    name = TextAreaField('Quizname',[validators.Length(min = 1, max = 100)], render_kw={'placeholder': 'Enter a quiz name'})
    description = TextAreaField('Description', render_kw={'placeholder': 'Decription of the quiz'})
    category = TextAreaField('Category',[validators.Length(max = 50)], render_kw={'placeholder': 'Enter a category'})

class questions(Form):
    quiz_id = HiddenField()
    question_text = TextAreaField('Question', validators=[DataRequired()])
    answer_1 = StringField('Answer 1', validators=[DataRequired()])
    correct_answer_1 = BooleanField([DataRequired()])
    answer_2 = StringField('Answer 2', validators=[DataRequired()])
    correct_answer_2 = BooleanField([DataRequired()])
    answer_3 = StringField('Answer 3', validators=[DataRequired()])
    correct_answer_3 = BooleanField([DataRequired()])
    answer_4 = StringField('Answer 4', validators=[DataRequired()])
    correct_answer_4 = BooleanField([DataRequired()])
    submit = SubmitField('Submit')
