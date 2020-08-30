import discord
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connected to database. SQLite3 v' + sqlite3.version)
    except Error as e:
        print(e)

    return conn

def check_user(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (message.author.id,))

        rows = cur.fetchall()
        if(len(rows) == 1):
            return True
        else:
            username = message.author.name+"#"+message.author.discriminator
            cur.execute("INSERT INTO users(id,name) VALUES (?,?)", (message.author.id,username))
            conn.commit()
            return False
    except Error as e:
        print(e)
