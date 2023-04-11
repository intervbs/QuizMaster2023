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
    
    def new_quiz(self, name, description, category, user_id):
        try:
            self.cursor.execute('insert into quiz (quiz_name, quiz_description, quiz_category, user_id) values (%s, %s, %s, %s)',
                                (name, description, category, user_id))
        except mysql.connector.Error as error:
            print(error)
        return
    
    def quiz_index(self):
        try:
            self.cursor.execute('select * from quiz')
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def quiz_q_and_a(self, quiz_id):
        try:
            self.cursor.execute('SELECT q.question_id, q.quiz_id, q.question_text, a.answer_id, a.answer_text FROM questions q JOIN answers a ON q.question_id = a.question_id WHERE q.quiz_id = %s', (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def quiz_add_question(self, quiz_id, question_text, 
                          a1, correct_answer_1, 
                          a2, correct_answer_2, 
                          a3, correct_answer_3,
                          a4, correct_answer_4):
        try:
            self.cursor.execute("INSERT INTO questions (quiz_id, question_text) VALUES (%s, %s)", (quiz_id, question_text))
            question_id = self.cursor.lastrowid
            print(question_id)
            self.cursor.execute("INSERT INTO answers (question_id, answer_text, is_correct) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)", (question_id, a1, correct_answer_1, question_id, a2, correct_answer_2, question_id, a3, correct_answer_3, question_id, a4, correct_answer_4))
        except mysql.connector.Error as error:
            print(error)
        return

    def quiz_hide_show(self, value):
        try:
            self.cursor.execute('update quiz set quiz_visible = (%s)', (value,))
        except mysql.connector.Error as error:
            print(error)
        return

        
        
