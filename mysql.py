import sys
import pymysql
from PyQt5.QtWidgets import *
import socket

localhost = socket.gethostname()
username = socket.gethostbyname(localhost)
print(localhost, username)

# Establish a connection to the MySQL server
connection = pymysql.connect(
    host='localhost', # 'local_ip
    user='username',
    password='0000',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Create a cursor
cur = connection.cursor()

def check_db(db_name):
    cur.execute("SHOW DATABASES LIKE %s", (db_name,))
    result = cur.fetchall()

    if len(result) == 0:
        cur.execute("CREATE DATABASE {}".format(db_name))
        print("[DB관리]", db_name, "Database Created")
    else:
        print("[DB관리]", db_name, "Database Already Exists")

if __name__ == "__main__":
    check_db("test")

# Don't forget to close the cursor and the connection when you're done
cur.close()
connection.close()
