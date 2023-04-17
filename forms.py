from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, EmailField, TextAreaField, SubmitField, BooleanField, HiddenField, SelectField 
from wtforms.validators import Email, InputRequired, EqualTo, DataRequired
from email_validator import validate_email, EmailNotValidError

class Login_user(FlaskForm):
    '''Form for login page'''
    username = StringField('Username', [validators.Length(min = 3, max = 63)], render_kw={'placeholder': 'Enter your username'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 255)], render_kw={'placeholder': 'Enter your password'})

class Reg_user(FlaskForm):
    '''Form for registrating a new user'''
    username = StringField('Username', [validators.Length(min = 3, max = 63)], render_kw={'placeholder': 'Enter your username'})
    firstname = StringField('First Name', [validators.Length(min = 1, max = 63)], render_kw={'placeholder': 'Enter your First Name'})
    lastname = StringField('Last Name', [validators.Length(min = 2, max = 63)], render_kw={'placeholder': 'Enter your Last Name'})
    email = EmailField('Email', validators=[validators.Length(min = 3, max = 255), Email(message='Please input a valid email')], render_kw={'placeholder': 'Enter your Email'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 255)], render_kw={'placeholder': 'Enter your password'})
    confirm = PasswordField('Repete Password', render_kw={'placeholder': 'Confirm your password'})

class New_quiz(FlaskForm):
    '''Form for making a new quiz'''
    name = TextAreaField('Quizname',[validators.Length(min = 1, max = 100)], render_kw={'placeholder': 'Enter a quiz name'})
    description = TextAreaField('Description', render_kw={'placeholder': 'Decription of the quiz'})
    category = TextAreaField('Category',[validators.Length(max = 50)], render_kw={'placeholder': 'Enter a category'})
    submit = SubmitField('Generate new quiz')

class questions(FlaskForm):
    user_id = HiddenField()
    quiz_id = HiddenField()
    question_id = HiddenField()
    question_text = TextAreaField('Question', validators=[DataRequired()])
    answer_1 = StringField('Answer 1', validators=[DataRequired()])
    correct_answer_1 = BooleanField()
    answer_2 = StringField('Answer 2', validators=[DataRequired()])
    correct_answer_2 = BooleanField()
    answer_3 = StringField('Answer 3', validators=[DataRequired()])
    correct_answer_3 = BooleanField()
    answer_4 = StringField('Answer 4', validators=[DataRequired()])
    correct_answer_4 = BooleanField()
    submit = SubmitField('Submit')
    update = SubmitField('Update')

class Answer(FlaskForm):
    user_id = HiddenField()
    question_id = HiddenField()
    quiz_id = HiddenField()
    question = TextAreaField('question', render_kw={'readonly': True})
    answer1 = TextAreaField('question', render_kw={'readonly': True})
    answer2 = TextAreaField('question', render_kw={'readonly': True})
    answer3 = TextAreaField('question', render_kw={'readonly': True})
    answer4 = TextAreaField('question', render_kw={'readonly': True})
    c_answer1 = BooleanField()
    c_answer2 = BooleanField()
    c_answer3 = BooleanField()
    c_answer4 = BooleanField()
    next = SubmitField('Next')
    save = SubmitField('Save Quiz')
    finish = SubmitField('Finish quiz')

class Select_quiz(FlaskForm):
    id = HiddenField()
    quiz_name = SelectField('Select a quiz', render_kw={'placeholder': 'Choose a quiz'})
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_quizzes = set()
        for quiz in args:
            if quiz.name not in unique_quizzes:
                self.quiz_name.choices.append((quiz.id, quiz.name))
                unique_quizzes.add(quiz.name)

class Select_question(FlaskForm):
    id = HiddenField()
    question = SelectField('Select a question', render_kw={'placeholder': 'Choose a quiz'})
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_questions = set()
        for question in args:
            if question.question_id not in unique_questions:
                self.question.choices.append((question.question_id, question.question))
                unique_questions.add(question.question)

class button(FlaskForm):
    command = HiddenField()
    button = SubmitField()