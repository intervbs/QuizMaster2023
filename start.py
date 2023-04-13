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
#@admin_required
def quiz():
    # Setup the dropdown menu for the quiz selection
    with myDB() as db:
        quiz_idx = db.get_quiz_index()
    q_i = [quiz_index(*x) for x in quiz_idx]
    quiz_choices = [(str(quiz.quiz_id), quiz.name) for quiz in q_i]
    form_quiz = forms.Select_quiz()
    form_quiz.quiz_name.choices = quiz_choices
    form_questions = forms.Select_question()
    form = forms.questions()
    
    if form_quiz.validate_on_submit() and request.form['form_type'] == 'quiz':
        quiz_id = form_quiz.quiz_name.data
        with myDB() as db:
            question_index = db.get_questions(quiz_id)
        q_q = [quiz_questions(*x) for x in question_index]
        question_choices = [(str(question.question_id), question.question) for question in q_q]
        form_questions.question.choices = question_choices
        print('HERE!!!!!!:',form_questions.question.choices)

        return render_template('quiz.html', form_quiz=form_quiz, form_questions=form_questions, form=form)
    elif form_questions.validate_on_submit() and request.form['form_type2'] == 'update':
        # Retrieve the selected question data from the database
        question_id = form_questions.question.data
        print('HERHERHERHEHREHRH: ',question_id)
        with myDB() as db:
            question_data = db.get_question_data(question_id)

        # Populate the form with the retrieved data
        form = forms.Update_question()
        form.question_text.data = question_data.question_text
        form.answer_1.data = question_data.answer_1
        form.correct_answer_1.data = question_data.correct_answer_1
        form.answer_2.data = question_data.answer_2
        form.correct_answer_2.data = question_data.correct_answer_2
        form.answer_3.data = question_data.answer_3
        form.correct_answer_3.data = question_data.correct_answer_3
        form.answer_4.data = question_data.answer_4
        form.correct_answer_4.data = question_data.correct_answer_4

        if form.validate_on_submit():
            # Update the question in the database with the new data
            with myDB() as db:
                db.update_question(question_id, form.question_text.data, form.answer_1.data, form.correct_answer_1.data,
                                    form.answer_2.data, form.correct_answer_2.data, form.answer_3.data, form.correct_answer_3.data,
                                    form.answer_4.data, form.correct_answer_4.data)

        return render_template('quiz.html', form_quiz=form_quiz, form_questions=form_questions, form=form)

    elif request.method == 'POST':
        # Add a new question to the database
        if form.validate_on_submit():
            with myDB() as db:
                db.add_question(form_questions.quiz_name.data, form.question_text.data, form.answer_1.data,
                                 form.correct_answer_1.data, form.answer_2.data, form.correct_answer_2.data,
                                 form.answer_3.data, form.correct_answer_3.data, form.answer_4.data,
                                 form.correct_answer_4.data)

        return render_template('quiz.html', form_quiz=form_quiz, form_questions=form_questions, form=form)

    return render_template('quiz.html', form_quiz=form_quiz, form_questions=form_questions, form=form)

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
@admin_required
def edit_quiz():
    '''Function to add, edit or delete questions in the quiz'''
    form = forms.questions()
    if form.validate_on_submit():
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
            db.add_question(quiz_id, question_text, answer_1, correct_answer_1, 
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