import os
import json

# Variables
prefix = "$"
dirPath = os.path.dirname(os.path.abspath(__file__))
confPath = dirPath + '/config.json'
dbPath = dirPath + '/snekbot.db'
config = json.load(open(confPath))
token = config['server'][0]['token']
ownerId = int(config['server'][0]['owner_id'])
moderatorId = config['server'][0]['moderator_id']

# Coffee Game
treePrice = config['game'][0]['tree_price']
landPrice = config['game'][0]['land_price']
harvestLimit = config['game'][0]['harvest_limit']
treesLimit = config['game'][0]['trees_limit']

# Colours
colourGeneral = 0x005064
colourSerious = 0xFF0000
colourModeration = 0xAF5EE7
colourCoffee = 0x734D26
