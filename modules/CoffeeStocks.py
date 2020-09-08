import asyncio
import math
import random
import sched, time
from utils import DatabaseController as db

minPrice = 10
maxPrice = 20

def setSellPrice(oldPrice):

    randoMin = 0.2
    randoMax = 1

    '''Check if price has potential to surge'''
    if random.randint(1, 5) == 5:
        priceMulti = 2
        randoMin = 0.65
    else:
        priceMulti = 1

    '''If price is almost hitting the minimum, force price to go up'''
    '''If price is almost hitting the maximum, force to go down'''
    if oldPrice < (minPrice + 1):
        newPrice = oldPrice + (random.uniform(randoMin, randoMax) * priceMulti)
    elif oldPrice > (maxPrice - 1):
        newPrice = oldPrice - (random.uniform(randoMin, randoMax) * priceMulti)
    else:
        '''Check trend trajectory. True for up, False for down'''
        if bool(random.getrandbits(1)) == True:
            '''Price goes up'''
            newPrice = oldPrice + (random.uniform(randoMin, randoMax) * priceMulti)
        else:
            '''Price goes down'''
            newPrice = oldPrice - (random.uniform(randoMin, randoMax) * priceMulti)

    '''Makes sure prices don't go past their min/max values'''
    if newPrice < minPrice:
        newPrice = minPrice
    if newPrice > maxPrice:
        newPrice = maxPrice

    newPrice = float("{:.2f}".format(newPrice))
    return newPrice

async def runCoffeeStocks(conn):
    while True:
        tickTime = time.time()
        if round(tickTime % 300) == 0:
            lastPrices = db.get_last_prices(conn, 1)
            oldPrice = lastPrices[0][0]
            newPrice = setSellPrice(oldPrice)
            db.insert_price_tick(tickTime, newPrice, conn)
            ''' Debug Only '''
            '''
            debugLastPrices = db.get_last_prices(conn, 1)
            debugNewestPrice = debugLastPrices[0][0]
            print(f'New stock price : {debugNewestPrice}')
            '''
            await asyncio.sleep(299)
        else:
            await asyncio.sleep(0.5)
