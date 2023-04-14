import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

class myDB:
    def __init__(self) -> None:
        db_config = {'host': 'localhost', 
                    'user': 'user',
                    'password': 'test',
                    'database': 'myDb'}
        self.configuration = db_config
        try:
            conn = mysql.connector.connect(**self.configuration)
        except mysql.connector.Error as error:
            print(f'Error connecting to MySQL database: {error}')
        finally:
            conn.close()

    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
    
    #############
    #   USERS   #
    #############

    def get_user(self, username):
        try:
            self.cursor.execute('SELECT * FROM accounts WHERE username = (%s)', (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as error:
                print(error)
        return result
    
    def get_user_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM accounts WHERE user_id = (%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as error:
                print(error)
        return result
    
    def add_new_user(self, username, password, firstname, lastname, email):
        try: 
            sql = 'insert into accounts (first_name, last_name, email, password, username) values (%s, %s, %s, %s, %s)'
            values = (firstname, lastname, email, generate_password_hash(password), username)
            self.cursor.execute(sql, values)
        except mysql.connector.Error as error:
             print(error)
        return
    
    ############
    #   QUIZ   #
    ############

    def get_quiz_index(self):
        try:
            self.cursor.execute('select * from quizzes')
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def add_new_quiz(self, name, description, category):
        try:
            self.cursor.execute('insert into quizzes (name, description, category) values (%s, %s, %s)', (name, description, category))
        except mysql.connector.Error as error:
            print(error)
        return
    
    def quiz_hide_show(self, quiz_id, value):
        try:
            self.cursor.execute('update quizzes set is_public = (%s) where quiz_id = %s', (value, quiz_id))
        except mysql.connector.Error as error:
            print(error)
        return

    #################
    #   QUESTIONS   #
    #################

    def get_questions(self, id):
        try:
            self.cursor.execute('SELECT * FROM questions WHERE quiz_id = %s', (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def get_question(self, id):
        try:
            self.cursor.execute('SELECT * FROM questions WHERE question_id = %s', (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def get_question_not_answered(self, user_id):
        try:
            self.cursor.execute('''SELECT q.* FROM questions q
                                    WHERE NOT EXISTS (SELECT 1 FROM answers a WHERE a.user_id = %s AND a.question_id = q.id)
                                    ORDER BY q.id ASC LIMIT 1''', (user_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def get_next_question_not_answered(self, user_id, question_id):
        try:
            self.cursor.execute('''SELECT q.* FROM questions q
                                    WHERE NOT EXISTS (SELECT 1 FROM answers a WHERE a.user_id = %s AND a.question_id = q.id)
                                    AND q.id > %s ORDER BY q.id ASC LIMIT 1''', (user_id, question_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def add_question(self, quiz_id, question_text, answer_1, correct_answer_1,
                   answer_2, correct_answer_2, answer_3, correct_answer_3,
                   answer_4, correct_answer_4):
        try:
            self.cursor.execute('''insert into questions 
                                (quiz_id, question_text, choice1_text, choice2_text, choice3_text, choice4_text, choice1_correct, choice2_correct, choice3_correct, choice4_correct	)
                                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                (quiz_id, question_text ,answer_1, answer_2, answer_3, answer_4, correct_answer_1, correct_answer_2, correct_answer_3, correct_answer_4))
        except mysql.connector.Error as error:
            print(error)
        return

    def quiz_answer(self, user_id, question_id, answer):
        try:
            self.cursor.execute('INSERT INTO answers (user_id, question_id, answer_text) VALUES (%s, %s, %s)', (user_id, question_id, answer))
        except mysql.connector.Error as error:
            print(error)
        return

    def update_question(self, test):
        try:
            print(test)
            sql = '''UPDATE questions SET 
                        question_text = (%s), 
                        choice1_text = (%s), 
                        choice2_text = (%s), 
                        choice3_text = (%s), 
                        choice4_text = (%s), 
                        choice1_correct = (%s), 
                        choice2_correct = (%s), 
                        choice3_correct = (%s), 
                        choice4_correct = (%s) 
                        WHERE question_id = (%s)'''
            self.cursor.execute(sql, test)
        except mysql.connector.Error as error:
            print(error)
        return
    
        
        
