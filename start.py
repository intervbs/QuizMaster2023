import forms
import secrets
from myDB import myDB
from user import User
from functools import wraps
from quiz import quiz_index, quiz_questions, all_users, all_user_answers
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = secrets.token_urlsafe(16)

#Error handling redirecting every error to index
@app.errorhandler(Exception)
def page_not_found(error):
    return redirect(url_for('index'))

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
    return render_template('login.html', login_form=login_form, title='Login')

@app.route('/loggedin', methods=['GET', 'POST'])
@login_required
def loggedin():
        '''When logged in the quizzes will be shown in a table'''
        # Some string manipulation for makeing the quiz public or not
        value = str(request.form.get('is_public')).replace('(','').replace(')','').replace(',','')
        delete = request.form.get('delete')
        x = value.split()
        with myDB() as db:
            if len(x) > 1:
                db.quiz_hide_show(x[0], x[1])        
            elif delete != None:
                db.delete_quiz(delete)
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
    # Gets the id for the quiz and 
    quiz_id = request.args.get('id')
    if quiz_id != None:
        with myDB() as db:
            result = db.get_quiz_num(quiz_id)
        quizidx = [quiz_index(*x) for x in result]
        return render_template('quiz.html', quizidx=quizidx)
    
@app.route('/questions', methods = ['GET', 'POST'])
@login_required
def questions():
    q_id = request.args.get('id')
    form_question = forms.Answer()
    form = forms.Answer()

    if form.validate_on_submit():
        user_id = form.user_id.data
        quiz_id = form.quiz_id.data
        q_id = form.question_id.data
        a1 = form.c_answer1.data
        a2 = form.c_answer2.data
        a3 = form.c_answer3.data
        a4 = form.c_answer4.data
        
        with myDB() as db:
            # Add the answe to the db and pulls up a new question
            values = (user_id, quiz_id, q_id, a1, a2, a3, a4)
            db.add_answer(values)
            result = db.get_next_question_not_answered(user_id, q_id, quiz_id)
        if len(result) > 0:
            # Makes the new question, if there is a question that is not answered
            question = quiz_questions(*result[0])   
            form_question = forms.Answer()
            form.process()
            form = forms.Answer()

            # Setup all the form data
            form.user_id.data = current_user.id
            form.quiz_id.data = question.quiz_id
            form.question_id.data = question.question_id
            form_question.question.data = question.question
            form_question.answer1.data = question.choice1
            form_question.answer2.data = question.choice2
            form_question.answer3.data = question.choice3
            form_question.answer4.data = question.choice4
            form.c_answer1.data = False
            form.c_answer2.data = False
            form.c_answer3.data = False
            form.c_answer4.data = False
            return render_template('questions.html', form_answer=form_question, form=form)
        else:
            return render_template('questions.html', id=current_user.id, qid=quiz_id)

    elif q_id != None:
        # when entering the page it will find the first question is there is any
        with myDB() as db:
            result = db.get_question_not_answered(current_user.id, q_id)
        if len(result) > 0:
            question = quiz_questions(*result[0])
            form.user_id.data = current_user.id
            form.quiz_id.data = question.quiz_id
            form.question_id.data = question.question_id
            form_question.question.data = question.question
            form_question.answer1.data = question.choice1
            form_question.answer2.data = question.choice2
            form_question.answer3.data = question.choice3
            form_question.answer4.data = question.choice4
        else:
            return render_template('questions.html', id=current_user.id, qid=q_id)
   
    return render_template('questions.html', form_answer=form_question, form=form)

@app.route('/save')
@login_required
def save():
    '''This function will take go throug all questions and answers and write them into a .txt file.
    The .txt will have the question, what the user answered and the correct answers'''
    user_id = request.args.get('id')
    quiz_id = request.args.get('qid')
    with myDB() as db:
        answers = db.get_user_answers(int(user_id), int(quiz_id))
    
    output = ''
    for row in answers:
        question_text = row[0]
        choice1_selected = row[1]
        choice2_selected = row[2]
        choice3_selected = row[3]
        choice4_selected = row[4]
        choice1_correct = row[5]
        choice2_correct = row[6]
        choice3_correct = row[7]
        choice4_correct = row[8]
        choice1_text    = row[9]
        choice2_text    = row[10]
        choice3_text    = row[11]
        choice4_text    = row[12]

        output += f"{question_text}\n"
        output += f"{choice1_text} Your Choice: {choice1_selected} (Correct: {choice1_correct})\n"
        output += f"{choice2_text} Your Choice: {choice2_selected} (Correct: {choice2_correct})\n"
        output += f"{choice3_text} Your Choice: {choice3_selected} (Correct: {choice3_correct})\n"
        output += f"{choice4_text} Your Choice: {choice4_selected} (Correct: {choice4_correct})\n\n"

    # Create a response object with the output as the file contents
    response = make_response(output)

    # Set the content type and headers to indicate that this is a text file download
    response.headers["Content-Type"] = "text/plain"
    response.headers["Content-Disposition"] = f"attachment; filename=quiz_results.txt"

    return response

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
        form_question = forms.Select_question()
        
        if form_quiz.validate_on_submit() and request.form['form_type'] == 'quiz':
            # Validates the information from the dropdown, then makes a list with all the questions
            quiz_id = form_quiz.quiz_name.data
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            
            return render_template('edit_quiz.html', form_quiz=form_quiz, form_question=form_question, form=form, q_q=q_q, quiz_id=quiz_id)

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

            return render_template('edit_quiz.html', form_quiz=form_quiz,  form=form, q_q=q_q, quiz_id=quiz_id)

    else:
        # Form for making a new question for the given quiz
        with myDB() as db:
            result = db.get_question(id)
            question = quiz_questions(*result[0])
            form_edit = forms.questions()
            form_edit.question_id.data = question.question_id
            form_edit.question_text.data = question.question
            form_edit.answer_1.data = question.choice1
            form_edit.answer_2.data = question.choice2
            form_edit.answer_3.data = question.choice3
            form_edit.answer_4.data = question.choice4
            form_edit.correct_answer_1.data = question.is_correct1
            form_edit.correct_answer_2.data = question.is_correct2
            form_edit.correct_answer_3.data = question.is_correct3
            form_edit.correct_answer_4.data = question.is_correct4
            print(form_edit.question_id.data)
            return render_template('edit_questions.html', form_edit=form_edit)

    return render_template('edit_quiz.html', form_quiz=form_quiz)


@app.route('/update', methods = ['GET', 'POST'])
@admin_required
def update():
    # handels the delete request from edit question
    delete = request.form.get('delete')
    if delete != None:
        with myDB() as db:
            print(delete)
            db.delete_question(delete)
            return redirect(url_for('edit_quiz'))
    form = forms.questions()

    if form.validate_on_submit():
        # Validates the form and update the question
        question_id     = int(form.question_id.data)
        question_text   = form.question_text.data.strip()
        answer_1        = form.answer_1.data.strip()
        answer_2        = form.answer_2.data.strip()
        answer_3        = form.answer_3.data.strip()
        answer_4        = form.answer_4.data.strip()
        correct_answer_1 = int(form.correct_answer_1.data)
        correct_answer_2 = int(form.correct_answer_2.data)
        correct_answer_3 = int(form.correct_answer_3.data)
        correct_answer_4 = int(form.correct_answer_4.data)
        values = (question_text, answer_1, answer_2, answer_3, answer_4, 
                  correct_answer_1, correct_answer_2, correct_answer_3,  correct_answer_4, question_id)
        with myDB() as db:
            db.update_question(values)
        return redirect(url_for('edit_quiz'))
    else:
        return render_template('edit_questions.html', form=form)
    
@app.route('/users', methods = ['GET', 'POST'])
@admin_required
def users():
    '''Handels the information for the admin to check the scores of a given user for any quizzes 
    they have taken'''
    user_id = request.args.get('id')
    quiz_id = request.args.get('qid')

    with myDB() as db:
        result = db.get_users()
        users = [all_users(*x) for x in result]

        if user_id != None and quiz_id == None:
            # Checks for all the quizzes the user have done
            result = db.get_all_quizzes(user_id)
            q_i = [quiz_index(*x) for x in result]
            return render_template('user.html', users=users, user_id=user_id, q_i=q_i)
        
        elif user_id != None and quiz_id != None:
            # Makes a qobject with all the answers the user has given
            with myDB() as db:
                answers = db.get_user_answers(int(user_id), int(quiz_id))
            output = [all_user_answers(*x) for x in answers]
            return render_template('user.html', output=output)          
        else:
            return render_template('user.html', users=users)   

if __name__ == '__main__':
    app.run()