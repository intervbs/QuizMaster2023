import forms
import secrets
from myDB import myDB
from user import User
from functools import wraps
from quiz import quiz_index, quiz_everything
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = secrets.token_urlsafe(16)

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
    login_form = forms.Login_user(request.form)
    if request.method == 'POST' and login_form.validate():
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
            db.quiz_hide_show(value)
        result = db.quiz_index()
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
    signup_form = forms.Reg_user(request.form)
    if request.method == 'POST' and signup_form.validate():
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
    quiz_id = request.form.get('quiz_id')
    with myDB() as db:
        result = db.quiz_q_and_a(quiz_id)
        print(result)
        if result is not None:
            if len(result) > 4:
                questions = quiz_everything()
                questions.questions_id = result[0]
                questions.quiz_id = result[1]
                questions.question = result[2]
                questions.answer_id = result[3]
                for i in range(len(result)):
                    questions.alt.append(result[i][4])
            return render_template('quiz.html', questions=questions)
        return render_template('quiz.html')

@app.route('/newquiz', methods=['GET', 'POST'])
@admin_required
def new_quiz():
    '''Create a new quiz only if you have the admin rights the adds it to the db'''
    new_quiz_form = forms.New_quiz(request.form)
    if request.method == 'POST' and new_quiz_form.validate():
        name        = new_quiz_form.name.data
        description = new_quiz_form.description.data
        category    = new_quiz_form.category.data
        with myDB() as db:
            db.new_quiz(name, description, category, current_user.id)
            return redirect(url_for('loggedin'))
    return render_template('newquiz.html', new_quiz_form=new_quiz_form, title='Make a new quiz')

@app.route('/editquiz', methods=['GET', 'POST'])
@admin_required
def edit_quiz():
    '''Function to add, edit or delete questions in the quiz'''
    quiz_id = request.args.get('quiz_id')
    print('DETTE er ARGS: ', quiz_id)
    form = forms.questions(request.form)
    if request.method == 'POST' and form.validate():
        question_text   = form.question_text.data
        answer_1        = form.answer_1.data
        answer_2        = form.answer_2.data
        answer_3        = form.answer_3.data
        answer_4        = form.answer_4.data
        correct_answer_1 = form.correct_answer_1.data
        correct_answer_2 = form.correct_answer_2.data
        correct_answer_3 = form.correct_answer_3.data
        correct_answer_4 = form.correct_answer_4.data
        with myDB() as db:
            print(quiz_id)
            quiz_id = request.args.get('quiz_id')
            print('Dette er en ID:',quiz_id)
            db.quiz_add_question(quiz_id, question_text, answer_1, correct_answer_1, 
                            answer_2, correct_answer_2, answer_3, correct_answer_3,
                            answer_4, correct_answer_4)
            flash('New question added to quiz!')
            return redirect(url_for('loggedin'))
    return render_template('edit_quiz.html', quiz_id=quiz_id, form=form)

@app.route('/update', methods = ['GET', 'POST'])
@admin_required
def update():
    pass

if __name__ == '__main__':
    app.run()