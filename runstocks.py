import Config as conf
from modules import CoffeeStocks as stk
from utils import DatabaseController as db

conn = db.create_connection(conf.dbPath)

stk.runCoffeeStocks(conn)
