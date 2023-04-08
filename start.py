import secrets
import forms
from myDB import myDB
from user import User
from flask import Flask, render_template, request, escape, redirect, url_for, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = secrets.token_urlsafe(16)

@login_manager.user_loader
def load_user(user_id):
    with myDB()as db:
        user = User(*db.get_user_by_id(user_id))
    return user

@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with myDB() as db:
            usr = db.get_user(username)
            if usr:
                user = User(*usr)
                if user.check_password(password):
                    login_user(user, remember=True)
                    return redirect(url_for('loggedin'))
        # If the authentication fails, return an error message to the user
        return render_template('login.html')
    # If the request method is GET, simply return the login page
    return render_template('login.html', title='Login')

@app.route('/loggedin')
@login_required
def loggedin():
    return render_template('loggedin.html')

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = forms.Reg_user(request.form)
    if request.method == 'POST' and signup_form.validate():
        username = signup_form.username.data
        password = signup_form.password.data
        firstname = signup_form.firstname.data
        lastname = signup_form.lastname.data
        email = signup_form.email.data
        with myDB() as db:
            db.add_new_user(username, password, firstname, lastname, email)
            return redirect(url_for('login'))
    return render_template('signup.html', signup_form=signup_form ,the_title = 'Sign Up')

if __name__ == '__main__':
    app.run()