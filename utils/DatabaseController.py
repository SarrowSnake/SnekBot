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
            cur.execute("INSERT INTO coffee(player,money,bags_dark,beans) VALUES (?,?,?,?)", (playerID,0,0,0))
            conn.commit()
            return False
    except Error as e:
        print(e)

def get_beans_leaderboards(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, beans_overall FROM users INNER JOIN coffee on users.id = coffee.player ORDER BY beans_overall DESC")
        rows = cur.fetchmany(10)
        return rows
    except Error as e:
        print(e)

def get_money_leaderboards(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, money FROM users INNER JOIN coffee on users.id = coffee.player ORDER BY money DESC")
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

def get_money(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT money FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        return record[0]
    except Error as e:
        print(e)
        return 0

def get_bags_dark(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT bags_dark FROM coffee WHERE player = ?", (message.author.id,))

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
        cur.execute("SELECT plant_date, beans, beans_overall FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        if(record[0] != 0 or (record is None)):
            cur.execute
            timeDelta = math.floor(time.time() - record[0])
            '''The multiplier in the future will be increased as planned upgrades get implemented.'''
            multiplier=1
            beanRate = (72/5)*multiplier
            minVal = math.floor((timeDelta/beanRate)*0.75)
            maxVal = math.floor(timeDelta/beanRate)
            harvestedBeans = random.randint(int(minVal), int(maxVal))
            totalBeans = harvestedBeans + int(record[1])
            overallBeans = record[2] + harvestedBeans
            cur.execute("UPDATE coffee SET plant_date=?, beans=?, beans_overall=? WHERE player=?", (0, totalBeans, overallBeans, message.author.id))
            conn.commit()
            return harvestedBeans
        else:
            return -1
    except Error as e:
        print(e)
        return -1

def roast_beans_dark(message, beans, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT beans, bags_dark FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        remainingBeans = record[0] - beans
        totalBags = record[1] + (beans/250)
        cur.execute("UPDATE coffee SET beans=?, bags_dark=? WHERE player=?", (remainingBeans, totalBags, message.author.id))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def sell_bags(message, bagsToSell, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT bags_dark, money FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        bagsRemaining = record[0] - bagsToSell
        if(bagsRemaining >= 0):
            earnedMoney = 0
            for x in range(bagsToSell):
                earnedMoney += random.randint(10, 15)
            totalMoney = record[1] + earnedMoney
            cur.execute("UPDATE coffee SET money=?, bags_dark=? WHERE player=?", (totalMoney, bagsRemaining, message.author.id))
            conn.commit()
            return earnedMoney
        else:
            return -1
    except Error as e:
        print(e)
        return -1
