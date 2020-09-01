import time
import math
import random

startTime = None

def __init__(self):
    return 0

def startFarming(message):
    startTime = time.time()

def harvest(message):
    global startTime

    harvestTime = time.time()
    timeDelta = harvestTime-startTime
    minHarvest = 0
    maxHarvest = math.floor(timeDelta/100)
    harvestRange = random.randint()
    print(maxHarvest)
