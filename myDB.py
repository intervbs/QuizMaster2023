import mysql.connector

class myDB:
    def __init__(self) -> None:
        db_config = {'host': 'localhost', 
                    'user': 'user',
                    'password': 'test',
                    'database': 'myDb'}
        self.configuration = db_config
        try:
            conn = mysql.connector.connect(**self.configuration)
            print('Connected to MySQL database')
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
            self.cursor.execute("SELECT * FROM accounts WHERE username=(%s)", (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def get_user_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM accounts WHERE userID=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result