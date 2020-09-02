import discord
import Config as conf
from discord.ext import commands
from modules import BaseCommands
from modules import CoffeeFarm
from utils import DatabaseController as db


conn = db.create_connection(conf.dbPath)
token = conf.token
client = commands.Bot(command_prefix=conf.prefix)

''' Initialize commands '''
bc = BaseCommands
bc.BaseCommands(client)
cf = CoffeeFarm
cf.CoffeeFarm(client, conn)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=conf.prefix+'help'))
    print('{0.user} is now running.'.format(client))
    channel = client.get_channel(744891551020482633)
    await channel.send('SnekBot booted up. Hello!')


@client.event
async def on_message(message):
    db.check_user(message, conn)
    global prefix
    global busy

    if message.author == client.user:
        return

    await client.process_commands(message)

client.run(token)
