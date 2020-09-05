import os
import json

prefix = "$"
dirPath = os.path.dirname(os.path.abspath(__file__))
confPath = dirPath + '/config.json'
dbPath = dirPath + '/snekbot.db'
config = json.load(open(confPath))
token = config['token']
ownerId = config['owner_id']
moderatorId = config['moderator_id']
