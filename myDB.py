import mysql.connector
import helper
from werkzeug.security import generate_password_hash

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

    def __enter__(self):
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
    
    def get_users(self):
        try:
            self.cursor.execute('SELECT * FROM accounts')
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
                print(error)
        return result
    
    def get_users_finished_quiz(self, quiz_id):
        try:
            self.cursor.execute('''SELECT DISTINCT accounts.*
                                    FROM accounts
                                    INNER JOIN answers ON accounts.user_id = answers.user_id
                                    WHERE answers.quiz_id = %s''', (quiz_id,))
            result = self.cursor.fetchall()
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
            sql = 'INSERT INTO accounts (first_name, last_name, email, password, username) VALUES (%s, %s, %s, %s, %s)'
            VALUES = (firstname, lastname, email, generate_password_hash(password), username)
            self.cursor.execute(sql, VALUES)
        except mysql.connector.Error as error:
             print(error)
    
    def add_admin(self, userid, is_admin):
        try:
            self.cursor.execute('update accounts set admin = %s where user_id = %s', (is_admin, userid,))
        except mysql.connector.Error as error:
            print(error)
        
    
    def check_user(self, username):
        try:
            self.cursor.execute('select * from accounts where username = %s', (username,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def check_email(self, email):
        try:
            self.cursor.execute('select * from accounts where email = %s', (email,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    ############
    #   QUIZ   #
    ############

    def get_quiz_num(self, id):
        try:
            self.cursor.execute('select * from quizzes where quiz_id = %s', (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result

    def get_quiz_index(self):
        try:
            self.cursor.execute('select * from quizzes')
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def add_new_quiz(self, name, description, category):
        try:
            self.cursor.execute('INSERT INTO quizzes (name, description, category) VALUES (%s, %s, %s)', (name, description, category))
        except mysql.connector.Error as error:
            print(error)
    
    def quiz_hide_show(self, quiz_id, value):
        try:
            if helper.check_if_quiz_is_approved(quiz_id):
                self.cursor.execute('update quizzes set is_public = (%s) where quiz_id = %s', (value, quiz_id,))
            if value == '0':
                self.cursor.execute('update quizzes set is_public = (%s) where quiz_id = %s', (value, quiz_id,))
        except mysql.connector.Error as error:
            print(error)

    def get_is_graded(self, user_id, quiz_id):
        try:
            self.cursor.execute('SELECT graded FROM quiz_graded WHERE user_id = %s and quiz_id = %s', (user_id, quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result

    def inser_quiz_graded_empty(self, user_id, quiz_id):
        try:
            self.cursor.execute('INSERT INTO quiz_graded (user_id, quiz_id) VALUES (%s, %s)', (user_id, quiz_id,))
            self.conn.commit()
            self.cursor.execute('select last_INSERT_id() as graded_id')
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result    

    def add_quiz_comment_graded(self, *args):
        try:
            self.cursor.execute('select graded_id from quiz_graded where user_id = %s and quiz_id = %s', (args[0], args[1],))
            result = self.cursor.fetchall()
            if len(result) < 1:
                self.inser_quiz_graded_empty(args[0], args[1])
                self.update_quiz_comment_graded(args[2], args[3], result[0][0])
            else:
                self.update_quiz_comment_graded(args[2], args[3], result[0][0])
        except mysql.connector.Error as error:
            print(error)

    def get_quiz_comment_graded(self, user_id, quiz_id):
        try:
            self.cursor.execute('select * from quiz_graded where user_id = (%s) and quiz_id = (%s)', (user_id, quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result

    def update_quiz_comment_graded(self, comment, graded, graded_id):
        try:
            self.cursor.execute('update quiz_graded set comment = %s, graded = %s where graded_id = %s', (comment, graded, graded_id,))
        except mysql.connector.Error as error:
            print(error)
    
    def open_close_quiz(self, quiz_id, is_open):
        try:
            self.cursor.execute('update quizzes set is_open = (%s) where quiz_id = (%s)', (is_open, quiz_id,))
        except mysql.connector.Error as error:
            print(error)

    def quiz_is_open(self, qid):
        try:
            self.cursor.execute('select is_open from quizzes where quiz_id = %s', (qid,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(error)
        return result

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
    
    def get_question_not_answered(self, user_id, quiz_id):
        try:
            self.cursor.execute('''SELECT q.* FROM questions q
                                    WHERE NOT EXISTS 
                                    (SELECT 1 FROM answers a WHERE a.user_id = %s AND a.question_id = q.question_id) 
                                    AND q.quiz_id = %s
                                    ORDER BY q.question_id ASC LIMIT 1''', (user_id, quiz_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def get_next_question_not_answered(self, user_id, question_id, quiz_id):
        try:
            self.cursor.execute('''SELECT q.* FROM questions q
                                    WHERE NOT EXISTS (SELECT 1 FROM answers a WHERE a.user_id = %s AND a.question_id = q.question_id)
                                    AND q.question_id > %s AND q.quiz_id = %s ORDER BY q.question_id ASC LIMIT 1''', (user_id, question_id, quiz_id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def get_question_not_approved(self, quiz_id):
        try:
            self.cursor.execute('SELECT * FROM questions WHERE quiz_id = %s AND question_approved = 0 LIMIT 1', (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def add_question(self, quiz_id, question_text, answer_1, correct_answer_1,
                   answer_2, correct_answer_2, answer_3, correct_answer_3,
                   answer_4, correct_answer_4, q_type):
        try:
            self.cursor.execute('''INSERT INTO questions 
                                (quiz_id, question_text, choice1_text, choice2_text, choice3_text, choice4_text, 
                                choice1_correct, choice2_correct, choice3_correct, choice4_correct, q_type	)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                (quiz_id, question_text ,answer_1, answer_2, answer_3, answer_4, correct_answer_1, correct_answer_2, correct_answer_3, correct_answer_4, q_type))
        except mysql.connector.Error as error:
            print(error)

    def approve_question(self, question_id):
        try:
            self.cursor.execute('UPDATE questions SET question_approved = 1 WHERE question_id =%s', (question_id,))
        except mysql.connector.Error as error:
            print(error)

    def update_question(self, test):
        try:
            sql = '''UPDATE questions SET 
                        question_text = (%s), 
                        choice1_text = (%s), 
                        choice2_text = (%s), 
                        choice3_text = (%s), 
                        choice4_text = (%s), 
                        choice1_correct = (%s), 
                        choice2_correct = (%s), 
                        choice3_correct = (%s), 
                        choice4_correct = (%s),
                        question_approved = (%s) 
                        WHERE question_id = (%s)'''
            self.cursor.execute(sql, test)
        except mysql.connector.Error as error:
            print(error)
    
    ###############
    #   ANSWERS   #
    ############### 

    def add_answer(self, VALUES):
        try:
            self.cursor.execute('''INSERT INTO answers (user_id, quiz_id, question_id, choice1_selected, choice2_selected, choice3_selected, choice4_selected, essay_answer)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', VALUES)
        except mysql.connector.Error as error:
            print(error)
    
    def add_answer_with_comment(self, VALUES, comment, graded):
        try:
            self.add_answer(VALUES)
            self.cursor.execute('SELECT LAST_INSERT_ID() AS answer_id')
            result = self.cursor.fetchall()
            self.update_comment(result[0][0], f'USER DID NOT COMPLETE THE QUIZ AND THE ANSWER IS NOT ANSWERED\n\n{comment}', graded)
        except mysql.connector.Error as error:
            print(error)

    def get_user_answers(self, user_id, question_id):
        try:
            sql ='''SELECT q.question_text,
                    q.q_type,
                    a.answer_id, 
                    a.choice1_selected, 
                    a.choice2_selected, 
                    a.choice3_selected, 
                    a.choice4_selected,
                    a.essay_answer,
                    a.comment,
                    a.graded,
                    q.choice1_correct,
                    q.choice2_correct,
                    q.choice3_correct,
                    q.choice4_correct,
                    q.choice1_text,
                    q.choice2_text,
                    q.choice3_text,
                    q.choice4_text
                    FROM answers a
                    JOIN questions q ON a.question_id = q.question_id
                    WHERE a.user_id = (%s) AND q.question_id = (%s)'''
            self.cursor.execute(sql, (user_id, question_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def get_all_user_answers(self, user_id, quiz_id):
        try:
            sql ='''SELECT q.question_text,
                    q.q_type,
                    a.answer_id, 
                    a.choice1_selected, 
                    a.choice2_selected, 
                    a.choice3_selected, 
                    a.choice4_selected,
                    a.essay_answer,
                    a.comment,
                    a.graded,
                    q.choice1_correct,
                    q.choice2_correct,
                    q.choice3_correct,
                    q.choice4_correct,
                    q.choice1_text,
                    q.choice2_text,
                    q.choice3_text,
                    q.choice4_text
                    FROM answers a
                    JOIN questions q ON a.question_id = q.question_id
                    WHERE a.user_id = (%s) AND q.quiz_id = (%s)'''
            self.cursor.execute(sql, (user_id, quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    def check_answer_is_graded(self, user_id, quiz_id):
        try:
            self.cursor.execute('SELECT graded FROM answers where user_id = %s and quiz_id = %s', (user_id, quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(error)
        return result
    
    ###############
    #   COMMENT   #
    ###############

    def update_comment(self, aid, comment, graded):
        try:
            self.cursor.execute('UPDATE answers SET comment = %s, graded = %s WHERE answer_id = %s', (comment, graded, aid,))
        except mysql.connector.Error as error:
            print(error)

    def update_quiz_graded(self, graded_id, graded):
        try:
            self.cursor.execute('UPDATE quiz_graded SET graded = %s where graded_id = %s', (graded, graded_id,))
        except mysql.connector.Error as error:
            print(error)

    ##############
    #   DELETE   #
    ##############

    def delete_quiz(self, quiz_id):
        try:
            self.cursor.execute('DELETE FROM quizzes WHERE quiz_id = (%s)', (quiz_id,))
            self.cursor.execute('DELETE FROM questions WHERE quiz_id = (%s)', (quiz_id,))
            self.cursor.execute('DELETE FROM answers WHERE quiz_id = (%s)', (quiz_id,))
            self.cursor.execute('DELETE FROM quiz_graded WHERE quiz_id = (%s)', (quiz_id,))
        except mysql.connector.Error as error:
            print(error)
    
    def delete_question(self, question_id):
        try:
            self.cursor.execute('DELETE FROM questions WHERE question_id = (%s)', (question_id,))
        except mysql.connector.Error as error:
            print(error)