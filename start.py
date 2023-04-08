import secrets
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

'''@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        password = request.form['password']
        username = request.form['username']
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, "firstname", "lastname", "user")', (username, password))
            connection.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg)
        cursor.close()
        connection.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', the_title = 'Register', msg=msg)'''

if __name__ == '__main__':
    app.run()