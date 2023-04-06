import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'test',
    'database': 'myDb'
}

try:
    conn = mysql.connector.connect(**db_config)
    print('Connected to MySQL database')
except mysql.connector.Error as error:
    print(f'Error connecting to MySQL database: {error}')
finally:
    conn.close()
