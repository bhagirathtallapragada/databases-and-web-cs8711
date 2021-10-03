#import mysql.connector
from mysql.connector import MySQLConnection, Error 
from python_mysql_dbconfig import read_db_config


def connect():
    """ Connect to MySQL database """
    db_config=read_db_config()
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)   
        #conn = mysql.connector.connect(host='localhost',
        #                               database='python_mysql',
        #                               user='root',
        #                               password='')
        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    connect()