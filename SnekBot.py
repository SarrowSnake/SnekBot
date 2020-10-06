import asyncio
import discord
import Config as conf
from discord.ext import commands
from modules import BaseCommands
from modules import CoffeeFarm
from modules import CoffeeShop
from modules import Moderation
from utils import DatabaseController as db


conn = db.create_connection(conf.dbPath)
token = conf.token
client = commands.Bot(command_prefix=conf.prefix)
client.remove_command('help')

''' Initialize commands '''
bc = BaseCommands
bc.BaseCommands(client)
cf = CoffeeFarm
cf.CoffeeFarm(client, conn)
cs = CoffeeShop
cs.CoffeeShop(client, conn)
mod = Moderation
mod.Moderation(client, conn)


async def verify(message):
    verifyString = "I have read the rules and agree to the server's policies"
    generalChannel = client.get_channel(744871234881454184)
    if(message.channel.id == 750720665270878279) and (message.author != client.user):
        if(message.content == verifyString or message.content == verifyString + "."):
            await message.delete()
            await message.author.add_roles(discord.utils.get(message.guild.roles, name='Member'), reason='User has verified.')
            await message.author.remove_roles(discord.utils.get(message.guild.roles, name='Verification'), reason='User has verified.')
            await generalChannel.send('Hello ' + message.author.mention + '! Welcome to the Coffee Pit. Enjoy your stay!')
        else:
            await message.delete()
            errorEmbed = discord.Embed(title='Wrong Passphrase.', description='The phrase you entered was mispelled/invalid. Please try again.', colour=conf.colourSerious)
            errorEmbed.set_footer(text=f'Your input : {message.content}')
            errorMessage = await message.channel.send(embed=errorEmbed)
            await asyncio.sleep(10)
            await errorMessage.delete()



async def suggestionListener(message):
    if (message.author == client.user) or (message.author.id == conf.ownerId):
        return
    else:
        if message.channel.id == 751851313226055701:
            upvoteEmoji = '\U0001F44D'
            await message.add_reaction(upvoteEmoji)

@client.event
async def on_ready():
    global stk
    botAvatar = client.user.avatar_url
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=conf.prefix+'help'))
    print('{0.user} is now running.'.format(client))
    channel = client.get_channel(744891551020482633)
    readyEmbed = discord.Embed(title='SnekBot Booted Up!', description='Hello!', colour=conf.colourGeneral)
    readyEmbed.set_thumbnail(url=botAvatar)
    await channel.send(embed=readyEmbed)


@client.event
async def on_message(message):
    await verify(message)
    await suggestionListener(message)
    db.check_user(message, conn)
    global prefix
    global busy

    if message.author == client.user:
        return

    await client.process_commands(message)

client.run(token)
