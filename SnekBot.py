import asyncio
import discord
import Config as conf
from discord.ext import commands
from modules import BaseCommands
from modules import CoffeeFarm
'''from modules import Moderation'''
from utils import DatabaseController as db


conn = db.create_connection(conf.dbPath)
token = conf.token
client = commands.Bot(command_prefix=conf.prefix)

''' Initialize commands '''
bc = BaseCommands
bc.BaseCommands(client)
cf = CoffeeFarm
cf.CoffeeFarm(client, conn)
'''
mod = Moderation
mod.Moderation(client, conn)
'''
async def verify(message):
    verifyString = "I have read the rules and agree to the server's policies"
    if(message.channel.id == 750720665270878279):
        if(message.content == verifyString):
            await message.delete()
            await message.author.add_roles(discord.utils.get(message.guild.roles, name='Member'), reason='User has verified.')
            await message.author.remove_roles(discord.utils.get(message.guild.roles, name='Verification'), reason='User has verified.')
        else:
            await message.delete()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=conf.prefix+'help'))
    print('{0.user} is now running.'.format(client))
    channel = client.get_channel(744891551020482633)
    await channel.send('SnekBot booted up. Hello!')


@client.event
async def on_message(message):
    await verify(message)
    db.check_user(message, conn)
    global prefix
    global busy

    if message.author == client.user:
        return

    await client.process_commands(message)

client.run(token)
