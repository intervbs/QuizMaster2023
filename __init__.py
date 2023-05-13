import forms
import secrets
import pdfkit
import helper
from myDB import myDB
from user import User
from functools import wraps
from quiz import quiz_index, quiz_questions, all_users, all_user_answers, answered_question
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_login import LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = secrets.token_urlsafe(16)

#Error handling redirecting every error to index
@app.errorhandler(Exception)
def page_not_found(error):
    return redirect(url_for('login'))

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
        # Some string manipulation for making the quiz public or not
        value = str(request.form.get('is_public')).replace('(','').replace(')','').replace(',','')
        open = str(request.form.get('is_open')).replace('(','').replace(')','').replace(',','')
        delete = request.form.get('delete')
        opn = open.split()
        x = value.split()
        with myDB() as db:
            if len(x) > 1:
                db.quiz_hide_show(x[0], x[1])        
            elif delete != None:
                db.delete_quiz(delete)
            elif len(opn) > 1:
                db.open_close_quiz(opn[0], opn[1])
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
        confirm     = signup_form.confirm.data
        if password != confirm:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
        with myDB() as db:
            user = db.check_user(username)
            mail = db.check_email(email)
            if user:
                flash('Username already taken')
                return redirect(url_for('signup'))
            elif mail:
                flash('Email already taken')
                return redirect(url_for('signup'))
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
        if request.form.get('form_type') == '1':
            form.c_answer1.data = 1
        elif request.form.get('form_type') == '2':
            form.c_answer2.data = 1
        elif request.form.get('form_type') == '3':
            form.c_answer3.data = 1
        elif request.form.get('form_type') == '4':
            form.c_answer4.data = 1

        user_id = form.user_id.data
        quiz_id = form.quiz_id.data
        q_id = form.question_id.data
        a1 = form.c_answer1.data
        a2 = form.c_answer2.data
        a3 = form.c_answer3.data
        a4 = form.c_answer4.data
        essay = form.essay_answer.data

        
        with myDB() as db:
            # Add the answe to the db and pulls up a new question
            values = (user_id, quiz_id, q_id, a1, a2, a3, a4, essay)
            db.add_answer(values)
            is_open = db.quiz_is_open(quiz_id)
            result = db.get_next_question_not_answered(user_id, q_id, quiz_id)
        if len(result) > 0 and is_open[0] == 1:
            # Makes the new question, if there is a question that is not answered
            question = quiz_questions(*result[0])   
            form_question.process()
            form.process()

            # Setup all the form data
            form.user_id.data = current_user.id
            form.quiz_id.data = question.quiz_id
            form.question_id.data = question.question_id
            form_question.question.data = question.question
            form_question.answer1.data = question.choice1
            form_question.answer2.data = question.choice2
            form_question.answer3.data = question.choice3
            form_question.answer4.data = question.choice4
            form_question.q_type = question.q_type
            form.c_answer1.data = False
            form.c_answer2.data = False
            form.c_answer3.data = False
            form.c_answer4.data = False
            return render_template('questions.html', form_question=form_question, form=form)
        else:
            with myDB() as db:
                graded = db.get_is_graded(current_user.id, quiz_id)
            return render_template('questions.html', id=current_user.id, qid=quiz_id, graded=graded[0][0])

    elif q_id != None:
        # when entering the page it will find the first question if there is any
        with myDB() as db:
            is_open = db.quiz_is_open(q_id)
            result = db.get_question_not_answered(current_user.id, q_id)
        if len(result) > 0 and is_open[0] == 1:
            question = quiz_questions(*result[0])
            form.user_id.data = current_user.id
            form.quiz_id.data = question.quiz_id
            form.question_id.data = question.question_id
            form_question.question.data = question.question
            form_question.answer1.data = question.choice1
            form_question.answer2.data = question.choice2
            form_question.answer3.data = question.choice3
            form_question.answer4.data = question.choice4
            form_question.q_type = question.q_type
        else:
            with myDB() as db:
                graded = db.get_is_graded(current_user.id, q_id)
                if len(graded) == 0:
                    graded.append([0,])
            return render_template('questions.html', id=current_user.id, qid=q_id, graded=graded[0][0])
   
    return render_template('questions.html', form_question=form_question, form=form)

@app.route('/save')
@login_required
def save():
    '''This function will take go throug all questions and answers and write them into a .txt file.
    The .txt will have the question, what the user answered and the correct answers'''
    user_id = request.args.get('id')
    quiz_id = request.args.get('qid')
    view = request.args.get('view')
    
    if view == '1':
        with myDB() as db:
            is_graded = db.get_quiz_comment_graded(user_id, quiz_id)
            if is_graded[0][4] == 1:
                quizname = db.get_quiz_num(quiz_id)
                results = db.get_all_user_answers(int(user_id), int(quiz_id))
                answers = [answered_question(*x) for x in results]
        form_graded = forms.graded()
        form_graded.comment.data = quizname[0][3]
        return render_template('save.html', form_graded=form_graded, answers=answers)

    
    output = helper.make_txt_file_for_download(user_id, quiz_id)

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
        form_essay = forms.questions()
        form_radio = forms.questions()
        form_question = forms.Select_question()
        
        if form_quiz.validate_on_submit() and request.form['form_type'] == 'quiz':
            # Validates the information from the dropdown, then makes a list with all the questions
            quiz_id = form_quiz.quiz_name.data
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            qc = [(str(q_c.question_id), q_c.question) for q_c in q_q]
            form_question.question.choices = qc
            
            return render_template('edit_quiz.html', form_quiz=form_quiz, form_question=form_question, form=form, form_essay=form_essay, q_q=q_q, quiz_id=quiz_id, form_radio=form_radio)

        elif form.validate_on_submit() and request.form['form_type'] == 'mc':
            # Add a new question to the database
            quiz_id = form.quiz_id.data
            with myDB() as db:
                db.add_question(quiz_id, form.question_text.data, form.answer_1.data,
                                form.correct_answer_1.data, form.answer_2.data, form.correct_answer_2.data,
                                form.answer_3.data, form.correct_answer_3.data, form.answer_4.data,
                                form.correct_answer_4.data, 0)
                    
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            form.process()
            form_essay.process()
            form_radio.process()

            return render_template('edit_quiz.html', form_quiz=form_quiz)
        
        elif form_essay.validate_on_submit() and request.form['form_type'] == 'essay':
            # Add a new question to the database
            quiz_id = form.quiz_id.data
            with myDB() as db:
                db.add_question(quiz_id, form.question_text.data, form_essay.answer_1.data,
                                form_essay.correct_answer_1.data, form_essay.answer_2.data, form_essay.correct_answer_2.data,
                                form_essay.answer_3.data, form_essay.correct_answer_3.data, form_essay.answer_4.data,
                                form_essay.correct_answer_4.data, 1)
                    
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            form.process()
            form_essay.process()
            form_radio.process()

            return render_template('edit_quiz.html', form_quiz=form_quiz)
        
        elif form_radio.validate_on_submit():
            # Add a new question to the database
            answer = request.form['form_type']
            # Check what radiobutton the is selected
            if answer == '1':
                form_radio.correct_answer_1.data = True
            elif answer == '2':
                form_radio.correct_answer_2.data = True
            elif answer == '3':
                form_radio.correct_answer_3.data = True
            elif answer == '4':
                form_radio.correct_answer_4.data = True

            quiz_id = form.quiz_id.data
            with myDB() as db:
                db.add_question(quiz_id, form_radio.question_text.data, form_radio.answer_1.data,
                                form_radio.correct_answer_1.data, form_radio.answer_2.data, form_radio.correct_answer_2.data,
                                form_radio.answer_3.data, form_radio.correct_answer_3.data, form_radio.answer_4.data,
                                form_radio.correct_answer_4.data, 2)
                    
            with myDB() as db:
                question_index = db.get_questions(quiz_id)
            q_q = [quiz_questions(*x) for x in question_index]
            form.process()
            form_essay.process()
            form_radio.process()

            return render_template('edit_quiz.html', form_quiz=form_quiz)

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
            form_edit.q_type = question.q_type
            form_edit.correct_answer_1.data = question.is_correct1
            form_edit.correct_answer_2.data = question.is_correct2
            form_edit.correct_answer_3.data = question.is_correct3
            form_edit.correct_answer_4.data = question.is_correct4
            return render_template('edit_questions.html', form_edit=form_edit)

    return render_template('edit_quiz.html', form_quiz=form_quiz)


@app.route('/update', methods = ['GET', 'POST'])
@admin_required
def update():
    # handels the delete request from edit question
    delete = request.form.get('delete')
    if delete != None:
        with myDB() as db:
            db.delete_question(delete)
            return redirect(url_for('edit_quiz'))
    form = forms.questions()

    # Sets the correct value from the radiobutton to the user answer
    if form.validate_on_submit():
        if request.form.get('form_type') == '1':
            form.correct_answer_1.data = 1
        elif request.form.get('form_type') == '2':
            form.correct_answer_2.data = 1
        elif request.form.get('form_type') == '3':
            form.correct_answer_3.data = 1
        elif request.form.get('form_type') == '4':
            form.correct_answer_4.data = 1

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
    # Setup the dropdown menu for the quiz selection
    with myDB() as db:
        quiz_idx = db.get_quiz_index()
    q_i = [quiz_index(*x) for x in quiz_idx]
    quiz_choices = [(str(quiz.quiz_id), quiz.name) for quiz in q_i]    
    form_quiz = forms.Select_quiz()
    form_quiz.quiz_name.choices = quiz_choices
    form_users = forms.Select_user()

    if form_quiz.validate_on_submit() and request.form['form_type'] == 'quiz':
        # Validates the information from the dropdown, then makes a list with all the users who have done the quiz
        quiz_id = form_quiz.quiz_name.data
        with myDB() as db:
            user_index = db.get_users_finished_quiz(quiz_id)
        all_user_index = [all_users(*x) for x in user_index]
        ui = [(str((u_i.user_id, int(quiz_id))), f'{u_i.firstname} {u_i.lastname}') for u_i in all_user_index]
        form_users.user.choices = ui
        
        return render_template('user.html', form_quiz=form_quiz, form_users=form_users, quiz_id=quiz_id)

    return render_template('user.html', form_quiz=form_quiz)

@app.route('/grade', methods = ['POST', 'GET'])
@admin_required
def grade():
    '''Grading the quiz'''
    id = str(request.args.get('id')).replace('(','').replace(')','').replace(',','')
    x = id.split()
    form_question = forms.Select_question()
    form_answer = forms.Answer_grade()
    form_graded = forms.graded()

    if request.method == 'POST' and request.form['form_type'] == 'graded':
        with myDB() as db:
            db.add_quiz_comment_graded(x[0], x[1], form_graded.comment.data, form_graded.is_graded.data)
            form_graded.process()
            quiz_graded = db.get_quiz_comment_graded(x[0], x[1])
            form_graded.comment.data = quiz_graded[0][3]

    if id != 'None':
        with myDB() as db:
            user = db.get_user_by_id(x[0])
            quiz = db.get_quiz_num(x[1])
            question_index = db.get_questions(x[1])
            answers_graded = db.check_answer_is_graded(x[0], x[1])
            quiz_graded = db.get_quiz_comment_graded(x[0], x[1])
            
            # Checks if the table have a answer for the quiz and user id. If there is no answer then it will be created
            if len(quiz_graded) > 0:
                form_graded.comment.data = quiz_graded[0][3]
            else:
                db.inser_quiz_graded_empty(x[0], x[1])
            
            # Sets the checkbox to True if all the answers have been graded
            form_graded.is_graded.data = helper.set_is_quiz_graded(x[0], x[1])
            
        q_q = [quiz_questions(*x) for x in question_index]
        qc = [(str(q_c.question_id), q_c.question) for q_c in q_q]
        form_question.question.choices = qc

    if request.method == 'POST' and request.form['form_type'] == 'question':
        qid = form_question.question.data
        with myDB() as db:
            result = db.get_user_answers(x[0], int(qid))
        if len(result) > 0:
            question = answered_question(*result[0])

            form_answer.user_id.data = x[0]
            form_answer.question_id.data = qid
            form_answer.aid.data = question.aid
            form_answer.q_type.data = question.q_type
            form_answer.q_txt.data = question.q_txt
            form_answer.choice_text1.data = question.c1_txt
            form_answer.choice_text2.data = question.c2_txt
            form_answer.choice_text3.data = question.c3_txt
            form_answer.choice_text4.data = question.c4_txt
            form_answer.essay_answer.data = question.a_essay
            form_answer.answer1.data = question.c1_cor
            form_answer.answer2.data = question.c2_cor
            form_answer.answer3.data = question.c3_cor
            form_answer.answer4.data = question.c4_cor
            form_answer.u_answer1.data = question.a1_sel
            form_answer.u_answer2.data = question.a2_sel
            form_answer.u_answer3.data = question.a3_sel
            form_answer.u_answer4.data = question.a4_sel
            if question.comment != None:
                form_answer.comment.data = question.comment
            if question.graded != None:
                form_answer.graded.data = question.graded
        
        else:
            # If the user did not complete the quiz and not every question is answered
            with myDB() as db:
                q = db.get_question(int(qid))
                question = quiz_questions(*q[0])
            form_answer.user_id.data = x[0]
            form_answer.quiz_id.data = x[1] 
            form_answer.question_id.data = qid
            form_answer.q_type.data = question.q_type
            form_answer.q_txt.data = question.question
            form_answer.choice_text1.data = 'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED'
            form_answer.choice_text2.data = 'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED'
            form_answer.choice_text3.data = 'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED'
            form_answer.choice_text4.data = 'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED'
            form_answer.essay_answer.data = 'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED'
            form_answer.answer1.data = question.is_correct1
            form_answer.answer2.data = question.is_correct2
            form_answer.answer3.data = question.is_correct3
            form_answer.answer4.data = question.is_correct4
            form_answer.u_answer1.data = False
            form_answer.u_answer2.data = False
            form_answer.u_answer3.data = False
            form_answer.u_answer4.data = False

    elif form_answer.validate_on_submit() and request.form['form_type'] == 'answer':
        if form_answer.aid.data != '':
            with myDB() as db:
                db.update_comment(form_answer.aid.data, form_answer.comment.data, form_answer.graded.data)
            form_answer.process()
            form_graded.is_graded.data = helper.set_is_quiz_graded(x[0], x[1])
        else:
            text = 'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED'
            with myDB() as db:
                db.add_answer_with_comment((form_answer.user_id.data, form_answer.quiz_id.data, form_answer.question_id.data, 
                              False, False, False, False, text,), form_answer.comment.data, form_answer.graded.data)
            form_answer.process()
            form_graded.is_graded.data = helper.set_is_quiz_graded(x[0], x[1])
        
    return render_template('grade.html', form_graded=form_graded, name=f'{user[1]} {user[2]}', quizname=quiz[0][1], form_question=form_question, form_answer=form_answer)

    
@app.route('/adminpanel', methods = ['POST', 'GET'])
@admin_required
def admin_panel():
    '''Where an admin can give another user admin rights'''
    value = str(request.form.get('is_admin')).replace('(','').replace(')','').replace(',','')
    x = value.split()

    with myDB() as db:         
        if len(x) > 1:
            db.add_admin(x[0], x[1])
        result = db.get_users()
        users = [all_users(*x) for x in result]

    return render_template('adminpanel.html', users=users) 

if __name__ == '__main__':
    app.run()