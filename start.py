import mysql.connector
import secrets
import re
from flask import Flask, render_template, request, escape, redirect, url_for, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


db_config = {'host': 'localhost', 
             'user': 'user',
             'password': 'test',
             'database': 'myDb'}
try:
    conn = mysql.connector.connect(**db_config)
    print('Connected to MySQL database')
except mysql.connector.Error as error:
    print(f'Error connecting to MySQL database: {error}')
finally:
    conn.close()

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

@app.route('/', methods=['GET'])
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT username FROM accounts')
    account = cursor.fetchone()
    if account:
        if session == None:
            logged_in = False
        else:
            logged_in = True
    return render_template('index.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['userID']
            session['username'] = account['username']
            session['fname'] = account['first_name']
            session['lname'] = account['last_name']
            return render_template('index2.html')
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', the_title = 'Login', msg=msg)
    
    return render_template('login.html', the_title = 'Login')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
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
    return render_template('register.html', the_title = 'Register', msg=msg)

if __name__ == '__main__':
    app.run()