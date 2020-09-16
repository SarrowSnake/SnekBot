import discord
import math
import random
import sqlite3
import time
import Config as conf
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
            cur.close()
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
            cur.execute("INSERT INTO coffee(player,money,beans,trees,land,bags,beans_overall) VALUES (?,?,?,?,?,?,?)", (playerID,0,0,1,1,0,0))
            conn.commit()
            cur.close()
            return False
    except Error as e:
        print(e)

def get_beans_leaderboards(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, beans_overall FROM users INNER JOIN coffee on users.id = coffee.player ORDER BY beans_overall DESC")
        rows = cur.fetchmany(10)
        cur.close()
        return rows
    except Error as e:
        print(e)

def get_money_leaderboards(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT name, money FROM users INNER JOIN coffee on users.id = coffee.player ORDER BY money DESC")
        rows = cur.fetchmany(10)
        cur.close()
        return rows
    except Error as e:
        print(e)

def get_beans(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT beans FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        cur.close()
        return record[0]
    except Error as e:
        print(e)
        return 0

def get_trees(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT trees FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        cur.close()
        return record[0]
    except Error as e:
        print(e)
        return 0

def get_land(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT land FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        cur.close()
        return record[0]
    except Error as e:
        print(e)
        return 0

def get_money(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT money FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        cur.close()
        return record[0]
    except Error as e:
        print(e)
        return 0

def get_bags(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT bags FROM coffee WHERE player = ?", (message.author.id,))

        record = cur.fetchone()
        cur.close()
        return record[0]
    except Error as e:
        print(e)
        return 0

def get_plant_status(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT plant_date FROM coffee WHERE player = ?", (message.author.id,))
        record = cur.fetchone()
        cur.close()
        if record[0] > 0:
            return True
        else:
            return False
    except Error as e:
        print(e)
        return False

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
        cur.close()

        return randNum
    except Error as e:
        print(e)
        return 0

def plant_beans(message, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT plant_date FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        checkEmpty = record[0]
        if(record[0] == None or record[0] == 0):
            cur.execute("UPDATE coffee SET plant_date=? WHERE player=?",( time.time(),message.author.id,))
            conn.commit()
            cur.close()
            return True
        else:
            cur.close()
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
            trees = get_trees(message, conn)
            '''The multiplier in the future will be increased as planned upgrades get implemented.'''
            multiplier=1
            beanRate = (162/5)*multiplier
            maxBeans = trees * conf.harvestLimit
            minVal = math.floor(trees*(timeDelta/beanRate)*0.75)
            maxVal = math.floor(trees*(timeDelta/beanRate))
            harvestedBeans = random.randint(int(minVal), int(maxVal))
            if harvestedBeans > maxBeans:
                harvestedBeans = maxBeans
            totalBeans = harvestedBeans + int(record[1])
            overallBeans = record[2] + harvestedBeans
            cur.execute("UPDATE coffee SET plant_date=?, beans=?, beans_overall=? WHERE player=?", (0, totalBeans, overallBeans, message.author.id))
            conn.commit()
            cur.close()
            return harvestedBeans
        else:
            cur.close()
            return -1
    except Error as e:
        print(e)
        return -1

def roast_beans(message, beans, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT beans, bags FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        remainingBeans = record[0] - beans
        totalBags = record[1] + (beans/250)
        cur.execute("UPDATE coffee SET beans=?, bags=? WHERE player=?", (remainingBeans, totalBags, message.author.id))
        conn.commit()
        cur.close()
        return True
    except Error as e:
        print(e)
        return False

def buy_trees(message, treesToBuy, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT money, trees FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        currentMoney = record[0]
        currentTrees = record[1]
        treeFees = treesToBuy * conf.treePrice
        newTrees = currentTrees + treesToBuy
        updatedMoney = currentMoney - treeFees
        cur.execute("UPDATE coffee SET trees=?, money=? WHERE player=?", (newTrees, updatedMoney, message.author.id))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
        return

def buy_land(message, landToBuy, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT money, land FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        currentMoney = record[0]
        currentLand = record[1]
        landFees = landToBuy * conf.landPrice
        newLand = currentLand + landToBuy
        updatedMoney = currentMoney - landFees
        cur.execute("UPDATE coffee SET trees=?, money=? WHERE player=?", (newLand, updatedMoney, message.author.id))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
        return


def sell_bags(message, bagsToSell, conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT bags, money FROM coffee WHERE player=?", (message.author.id,))
        record = cur.fetchone()
        bagsRemaining = record[0] - bagsToSell
        if(bagsRemaining >= 0):
            lastPrice = get_last_prices(conn, 1)
            earnedMoney = lastPrice[0][0]*bagsToSell
            totalMoney = record[1] + earnedMoney
            cur.execute("UPDATE coffee SET money=?, bags=? WHERE player=?", (totalMoney, bagsRemaining, message.author.id))
            conn.commit()
            cur.close()
            return earnedMoney
        else:
            cur.close()
            return -1
    except Error as e:
        print(e)
        return -1

def insert_price_tick(time, price, conn):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO stocks(time, price) VALUES (?,?)", (time, price))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)

def get_last_prices(conn, amount):
    try:
        cur = conn.cursor()
        cur.execute("SELECT price FROM stocks ORDER BY stock_tick_id DESC")
        records = cur.fetchmany(amount)
        cur.close()
        return records
    except Error as e:
        print(e)
        return None
