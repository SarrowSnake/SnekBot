import discord
import math
import random
import sqlite3
import time
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

def check_player(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT beans FROM coffee WHERE player = ?", (message.author.id,))

        rows = cur.fetchall()
        if(len(rows) == 1):
            return True
        else:
            playerID = message.author.id
            cur.execute("INSERT INTO coffee(player,beans) VALUES (?,?)", (playerID,0))
            conn.commit()
            return False
    except Error as e:
        print(e)

def get_leaderboards(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, beans FROM users INNER JOIN coffee on users.id = coffee.player ORDER BY beans DESC")
        rows = cur.fetchmany(10)
        return rows
    except Error as e:
        print(e)

def get_beans(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT beans FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        return record[0]
    except Error as e:
        print(e)
        return 0

def make_beans(message, conn):
    try:
        randNum = random.randint(-40, 50)
        cur = conn.cursor()
        cur.execute("SELECT beans FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        newBeans = record[0] + randNum
        if(newBeans < 0):
            newBeans = 0
        cur.execute("UPDATE coffee SET beans=? WHERE player=?", (newBeans,message.author.id,))
        conn.commit()

        return randNum
    except Error as e:
        print(e)
        return 0

def plant_beans(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT plant_date FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        print(record)
        if(record[0] == None or record[0] == 0):
            cur.execute("UPDATE coffee SET plant_date=? WHERE player=?",( time.time(),message.author.id,))
            conn.commit()
            return True
        else:
            return False
    except Error as e:
        print(e)
        return False

def harvest_beans(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT plant_date, beans FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        if(record[0] != 0 or (record is None)):
            cur.execute
            timeDelta = math.floor(time.time() - record[0])
            print('TimeDelta : ' + str(timeDelta))
            '''The multiplier in the future will be increased as planned upgrades get implemented.'''
            multiplier=1
            beanRate = (72/5)*multiplier
            minVal = math.floor((timeDelta/beanRate)*0.75)
            maxVal = math.floor(timeDelta/beanRate)
            harvestedBeans = random.randint(int(minVal), int(maxVal))
            totalBeans = harvestedBeans + int(record[1])
            cur.execute("UPDATE coffee SET plant_date=?, beans=? WHERE player=?",(0,harvestedBeans,message.author.id))
            conn.commit()
            return harvestedBeans
        else:
            return -1
    except Error as e:
        print(e)
        return -1
