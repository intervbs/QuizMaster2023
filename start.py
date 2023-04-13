import forms
import secrets
from myDB import myDB
from user import User
from functools import wraps
from quiz import quiz_index, quiz_questions
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = secrets.token_urlsafe(16)

#Error handling
'''@app.errorhandler(Exception)
def page_not_found(error):
    return redirect(url_for('index'))'''

@login_manager.user_loader
def load_user(user_id):
    with myDB()as db:
        user = User(*db.get_user_by_id(user_id))
    return user

def admin_required(func):
    '''Made my own wrapper to check for admin rights'''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view

@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome')

@app.route('/login', methods =['GET', 'POST'])
def login():
    '''Login function, using forms and checking the information against the db'''
    login_form = forms.Login_user()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data        
        if User.login(username, password):
            return redirect(url_for('loggedin'))
    # If the request method is GET, simply return the login page
    return render_template('login.html', login_form=login_form, title='Login')

@app.route('/loggedin', methods=['GET', 'POST'])
@login_required
def loggedin():
        '''When logged in the quizzes will be shown in a table'''
        with myDB() as db:
            value = request.form.get('visible')
            if value != None:
                db.quiz_hide_show(value[1], value[4])
            result = db.get_quiz_index()
        quizidx = [quiz_index(*x) for x in result]
        return render_template('loggedin.html', quizidx=quizidx)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Sign Up function, using forms and validates them then adds a new user to the db'''
    signup_form = forms.Reg_user()
    if signup_form.validate_on_submit():
        username    = signup_form.username.data
        password    = signup_form.password.data
        firstname   = signup_form.firstname.data
        lastname    = signup_form.lastname.data
        email       = signup_form.email.data
        with myDB() as db:
            db.add_new_user(username, password, firstname, lastname, email)
            return redirect(url_for('login'))
    return render_template('signup.html', signup_form=signup_form ,the_title = 'Sign Up')

@app.route('/quiz', methods = ['GET', 'POST'])
@login_required
def quiz():
    pass


@app.route('/empty', methods=["GET", "POST"])
def empty():
    return render_template('empty.html')

@app.route('/newquiz', methods=['GET', 'POST'])
@admin_required
def new_quiz():
    '''Create a new quiz only if you have the admin rights then adds it to the db'''
    form = forms.New_quiz()
    if form.validate_on_submit():
        name        = form.name.data.strip()
        description = form.description.data.strip()
        category    = form.category.data.strip()
        print(name, description, category)
        with myDB() as db:
            db.add_new_quiz(name, description, category)
            return redirect(url_for('loggedin'))
    return render_template('newquiz.html', form=form, title='Make a new quiz')

@app.route('/editquiz', methods=['GET', 'POST'])
#@admin_required
def edit_quiz():
    '''Function to add, edit or delete questions in the quiz'''
    id = request.args.get('id')
    
    if not id:
        # Setup the dropdown menu for the quiz selection
        with myDB() as db:
            quiz_idx = db.get_quiz_index()
        q_i = [quiz_index(*x) for x in quiz_idx]
        quiz_choices = [(str(quiz.quiz_id), quiz.name) for quiz in q_i]
        form_quiz = forms.Select_quiz()
        form_quiz.quiz_name.choices = quiz_choices
        form = forms.questions()
        
        if form_quiz.validate_on_submit() and request.form['form_type'] == 'quiz':
            quiz_id = form_quiz.quiz_name.data
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            print(quiz_id)
            return render_template('edit_quiz.html', form_quiz=form_quiz, form=form, q_q=q_q, quiz_id=quiz_id)

        elif form.validate_on_submit():
            # Add a new question to the database
            print(form.quiz_id.data)
            quiz_id = form.quiz_id.data
            with myDB() as db:
                db.add_question(quiz_id, form.question_text.data, form.answer_1.data,
                                form.correct_answer_1.data, form.answer_2.data, form.correct_answer_2.data,
                                form.answer_3.data, form.correct_answer_3.data, form.answer_4.data,
                                form.correct_answer_4.data)
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            form.process()

            return render_template('edit_quiz.html', form_quiz=form_quiz, form=form, q_q=q_q, quiz_id=quiz_id)

    return render_template('edit_quiz.html', form_quiz=form_quiz)


@app.route('/update', methods = ['GET', 'POST'])
@admin_required
def update():
    pass

if __name__ == '__main__':
    app.run()