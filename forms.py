from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, EmailField, TextAreaField, SubmitField, BooleanField, HiddenField, SelectField, RadioField
from wtforms.validators import Email, InputRequired, EqualTo, DataRequired
from email_validator import validate_email, EmailNotValidError

class Login_user(FlaskForm):
    '''Form for login page'''
    username = StringField('Username', [validators.Length(min = 3, max = 63)], render_kw={'placeholder': 'Enter your username', 'style': 'background-color: #edf0f5;'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 255)], render_kw={'placeholder': 'Enter your password', 'style': 'background-color: #edf0f5;'})

class Reg_user(FlaskForm):
    '''Form for registrating a new user'''
    username = StringField('Username', [validators.Length(min = 3, max = 63)], render_kw={'placeholder': 'Enter your username', 'style': 'background-color: #edf0f5;'})
    firstname = StringField('First Name', [validators.Length(min = 1, max = 63)], render_kw={'placeholder': 'Enter your First Name', 'style': 'background-color: #edf0f5;'})
    lastname = StringField('Last Name', [validators.Length(min = 2, max = 63)], render_kw={'placeholder': 'Enter your Last Name', 'style': 'background-color: #edf0f5;'})
    email = EmailField('Email', validators=[validators.Length(min = 3, max = 255), Email(message='Please input a valid email')], render_kw={'placeholder': 'Enter your Email', 'style': 'background-color: #edf0f5;'})
    password = PasswordField('Password', [validators.Length(min = 3, max = 255)], render_kw={'placeholder': 'Enter your password', 'style': 'background-color: #edf0f5;'})
    confirm = PasswordField('Repete Password', render_kw={'placeholder': 'Confirm your password', 'style': 'background-color: #edf0f5;'})

class New_quiz(FlaskForm):
    '''Form for making a new quiz'''
    name = TextAreaField('Quizname',[validators.Length(min = 1, max = 100)], render_kw={'placeholder': 'Enter a quiz name', 'style': 'background-color: #edf0f5;'})
    description = TextAreaField('Description', render_kw={'placeholder': 'Decription of the quiz', 'style': 'background-color: #edf0f5;'})
    category = TextAreaField('Category',[validators.Length(max = 50)], render_kw={'placeholder': 'Enter a category', 'style': 'background-color: #edf0f5;'})
    submit = SubmitField('Generate new quiz')

class graded(FlaskForm):
    user_id = HiddenField()
    quiz_id = HiddenField()
    is_graded = BooleanField('Graded',render_kw={'style': 'background-color: #edf0f5;'})
    comment = TextAreaField('Comment Quiz', render_kw={'style': 'background-color: #edf0f5;'})
    submit = SubmitField('Finish Grading Quiz')

class questions(FlaskForm):
    user_id = HiddenField()
    quiz_id = HiddenField()
    question_id = HiddenField()
    question_text = TextAreaField('Question', validators=[DataRequired()], render_kw={'style': 'background-color: #edf0f5;'})
    answer_1 = StringField('Answer 1', validators=[InputRequired()], render_kw={'style': 'background-color: #edf0f5;'})
    answer_2 = StringField('Answer 2', validators=[InputRequired()], render_kw={'style': 'background-color: #edf0f5;'})
    answer_3 = StringField('Answer 3', validators=[InputRequired()], render_kw={'style': 'background-color: #edf0f5;'})
    answer_4 = StringField('Answer 4', validators=[InputRequired()], render_kw={'style': 'background-color: #edf0f5;'})
    correct_answer_1 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    correct_answer_2 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    correct_answer_3 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    correct_answer_4 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    q_type = HiddenField()
    submit = SubmitField('Submit')
    update = SubmitField('Update')

class Answer(FlaskForm):
    user_id = HiddenField()
    question_id = HiddenField()
    quiz_id = HiddenField()
    q_type = HiddenField()
    question = TextAreaField('Question', render_kw={'readonly': True, 'style': 'background-color: #edf0f5;'})
    answer1 = TextAreaField('question', render_kw={'readonly': True, 'style': 'background-color: #edf0f5;'})
    answer2 = TextAreaField('question', render_kw={'readonly': True, 'style': 'background-color: #edf0f5;'})
    answer3 = TextAreaField('question', render_kw={'readonly': True, 'style': 'background-color: #edf0f5;'})
    answer4 = TextAreaField('question', render_kw={'readonly': True, 'style': 'background-color: #edf0f5;'})
    essay_answer = TextAreaField('Answer', render_kw={'style': 'background-color: #edf0f5;'})
    c_answer1 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    c_answer2 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    c_answer3 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    c_answer4 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    comment = TextAreaField(render_kw={'style': 'background-color: #edf0f5;'})
    next = SubmitField('Next')
    save = SubmitField('Save Quiz')
    finish = SubmitField('Finish quiz')

class Answer_grade(FlaskForm):
    user_id = HiddenField()
    question_id = HiddenField()
    quiz_id = HiddenField()
    aid = HiddenField()
    q_type = HiddenField()
    q_txt = TextAreaField(render_kw={'style': 'background-color: #edf0f5;', 'readonly': True})
    answer1 = BooleanField('Correct Answer', render_kw={'style': 'background-color: #edf0f5;'})
    answer2 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    answer3 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    answer4 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    choice_text1 = TextAreaField(render_kw={'style': 'background-color: #edf0f5;', 'readonly': True})
    choice_text2 = TextAreaField(render_kw={'style': 'background-color: #edf0f5;', 'readonly': True})
    choice_text3 = TextAreaField(render_kw={'style': 'background-color: #edf0f5;', 'readonly': True})
    choice_text4 = TextAreaField(render_kw={'style': 'background-color: #edf0f5;', 'readonly': True})
    essay_answer = TextAreaField('Answer', render_kw={'style': 'background-color: #edf0f5;', 'readonly': True})
    u_answer1 = BooleanField('User Choice', render_kw={'style': 'background-color: #edf0f5;'})
    u_answer2 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    u_answer3 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    u_answer4 = BooleanField(render_kw={'style': 'background-color: #edf0f5;'})
    comment = TextAreaField('Comment', render_kw={'style': 'background-color: #edf0f5;'})
    update = SubmitField('Update')

class Select_quiz(FlaskForm):
    id = HiddenField()
    quiz_name = SelectField('Select a quiz', render_kw={'placeholder': 'Choose a quiz', 'style': 'background-color: #edf0f5;'})
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
    question = SelectField('Select a question', render_kw={'placeholder': 'Choose a quiz', 'style': 'background-color: #edf0f5;'})
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_questions = set()
        for question in args:
            if question.question_id not in unique_questions:
                self.question.choices.append((question.question_id, question.question))
                unique_questions.add(question.question)

class Select_user(FlaskForm):
    id = HiddenField()
    user = SelectField('Select a quiz', render_kw={'placeholder': 'Choose a quiz', 'style': 'background-color: #edf0f5;'})
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_users = set()
        for user in args:
            if user.username not in unique_users:
                self.user.choices.append((user.user_id, user.username))
                unique_users.add(user.username)

class button(FlaskForm):
    command = HiddenField()
    button = SubmitField()