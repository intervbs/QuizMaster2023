from myDB import myDB
from werkzeug.security import check_password_hash
from flask_login import login_user
import mysql.connector


class User():
    # construct / attributes
    def __init__(self, id, firstname, lastname, email, passwordHash, username, admin):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.passwordHash = passwordHash.replace("\'", "")
        self.username = username
        self.is_admin = admin
        self.is_authenticated = True
        self.is_active= True
        self.is_anonymous = False

    @staticmethod
    def login(username, password):
        with myDB() as db:
            usr = db.get_user(username)
            if usr:
                user = User(*usr)
                if check_password_hash(user.passwordHash, password):
                    login_user(user, remember=True)
                    return True
            return False

    def __str__(self):
        return f'Id: {self.id}\n' + \
               f'Username: {self.username}\n' + \
               f'Email: {self.email}\n' + \
               f'Password Hash: {self.passwordHash}'

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get(self,id):
        with myDB() as db:
            user = User(*db.get_user_by_id(id))
            if user:
                return user
            else:
                return False
            
    def get_user_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM user WHERE  userID=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result