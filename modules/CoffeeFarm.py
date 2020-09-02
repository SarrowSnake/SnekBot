import asyncio
import discord
import time
import math
import random
import Config
from utils import DatabaseController as db

busy = False

def CoffeeFarm(client, conn):

    global busy
    global db

    @client.command()
    async def beans(ctx):
        if(db.check_player(ctx.message,conn) == False):
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Welcome new player!')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('You currently have no coffee beans, but you\'ll get more soon!')
        else:
            beans = db.get_beans(ctx.message, conn)
            await ctx.message.channel.send('You have ' + f'{beans:,}' + ' grams of coffee beans')

    @client.command()
    async def getbeans(ctx):
        if(db.check_player(ctx.message,conn) == False):
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Welcome new player!')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('You currently have no coffee beans, but you\'ll get more soon!')
        else:
            newBeans = db.make_beans(ctx.message, conn)
            if(newBeans > 0):
                await ctx.message.channel.send('You got ' + str(newBeans) + ' grams of beans!')
            elif(newBeans < 0):
                await ctx.message.channel.send('You lost ' + str(newBeans*-1) + ' grams of beans. :(')
            else:
                await ctx.message.channel.send('You didn\'t get any beans.')

    @client.command()
    async def leaderboards(ctx):
        results = db.get_leaderboards(conn)
        outputString = ""
        for result in results:
            if(result[1] > 0):
                name = result[0]
                beans = str(result[1])
                outputString = outputString + ("**" + name + "** with **" + beans + "** grams of beans.\n")
        leaderEmbed = discord.Embed(title='Leaderboards - Top 10',description=outputString,colour=0x005064)
        await ctx.message.channel.send(embed=leaderEmbed)

    @client.command()
    async def plant(ctx):
        if(db.check_player(ctx.message,conn) == False):
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Welcome new player!')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('You currently have no coffee beans, but you\'ll get more soon!')
        else:
            if(db.plant_beans(ctx.message, conn)):
                await ctx.message.channel.send('Your coffee seeds have been planted! Please wait a while until it\'s ready to harvest.')
            else:
                await ctx.message.channel.send('You\'ve already planted a tree!')

    @client.command()
    async def harvest(ctx):
        if(db.check_player(ctx.message,conn) == False):
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Welcome new player!')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('You currently have no coffee beans, but you\'ll get more soon!')
        else:
            harvestedBeans = db.harvest_beans(ctx.message, conn)
            if(harvestedBeans >= 0):
                ''' Harvest algorithm here '''
                await ctx.message.channel.send('You harvested your coffee trees and got ' + str(harvestedBeans) + ' grams of beans!')
            else:
                await ctx.message.channel.send('Something went wrong.')
