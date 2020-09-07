import asyncio
import discord
import time
import math
import random
import Config
from utils import DatabaseController as db

busy = False


async def introMessage(message):
    async with message.channel.typing():
        await asyncio.sleep(3)
    await message.channel.send('Welcome new player!')
    async with message.channel.typing():
        await asyncio.sleep(3)
    await message.channel.send('You currently have no coffee beans, but you\'ll get more soon!')
    async with message.channel.typing():
        await asyncio.sleep(3)
    await message.channel.send('Start planting trees to harvest more coffee beans with ``$plant``!')


def CoffeeFarm(client, conn):

    global busy
    global db

    @client.command()
    async def beans(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await introMessage(ctx.message)
        else:
            beans = db.get_beans(ctx.message, conn)
            await ctx.message.channel.send('You have **' + f'{beans:,}' + '** grams of green beans')

    @client.command()
    async def money(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await introMessage(ctx.message)
        else:
            money = db.get_money(ctx.message, conn)
            await ctx.message.channel.send('You have **$' + f'{money:,}' + '**')

    @client.command()
    async def leaderboards(ctx, arg):
        db.check_user(ctx.message, conn)
        if(arg.lower() == 'beans'):
            results = db.get_beans_leaderboards(conn)
            outputString = ""
            for result in results:
                if(result[1] > 0):
                    name = result[0]
                    beans = result[1]
                    outputString = outputString + ("**" + name + "** with **" + f'{beans:,}' + "** grams of green beans.\n")
            leaderEmbed = discord.Embed(title='Leaderboards - Top 10 Coffee Producer', description=outputString, colour=0x005064)
            await ctx.message.channel.send(embed=leaderEmbed)
        elif(arg.lower() == 'money'):
            results = db.get_money_leaderboards(conn)
            outputString = ""
            for result in results:
                if(result[1] > 0):
                    name = result[0]
                    money = result[1]
                    outputString = outputString + ("**" + name + "** with **$" + f'{money:,}' + "**\n")
            leaderEmbed = discord.Embed(title='Leaderboards - Top 10 Wealthiest', description=outputString, colour=0x005064)
            await ctx.message.channel.send(embed=leaderEmbed)
        else:
            await ctx.message.channel.send('Can\'t retrive leaderboards. Try adding ``beans`` or ``money`` at the end of the command.')

    @client.command()
    async def plant(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Welcome new player!')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('You currently have no coffee beans, but you\'ll get more soon!')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
        if(db.plant_beans(ctx.message, conn)):
            await ctx.message.channel.send('Your coffee tree have been planted! Please wait a while until it\'s ready to harvest.')
        else:
            await ctx.message.channel.send('You\'ve already planted a tree!')

    @client.command()
    async def harvest(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await introMessage(ctx.message)
        else:
            harvestedBeans = db.harvest_beans(ctx.message, conn)
            if(harvestedBeans >= 0):
                ''' Harvest algorithm here '''
                await ctx.message.channel.send('You harvested your coffee trees and got **' + f'{harvestedBeans:,}' + '** grams of green beans!')
            else:
                await ctx.message.channel.send('You haven\'t ``$plant``ed any trees yet! .')

    @client.command()
    async def bags(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await introMessage(ctx.message)
        else:
            bags = db.get_bags_dark(ctx.message, conn)
            await ctx.message.channel.send('[Dark Roast] You have **' + f'{bags:,}' + '** bags.')

    @client.command()
    async def roast(ctx, *arg):
        try:
            db.check_user(ctx.message, conn)
            if(len(arg) == 1):
                bags = math.floor(int(arg[0]))
                if(bags < 1):
                    await ctx.message.channel.send('The amount of bags you specified isn\'t possible. Defaulting to **1**.')
                    bags = 1
            elif(len(arg) == 0):
                bags = 1
            else:
                await ctx.message.channel.send('Too many arguments. Use ``$roast`` or ``$roast [number]``')
                return
            if not(db.check_player(ctx.message, conn)):
                await introMessage(ctx.message)
            else:
                currGreenBeans = db.get_beans(ctx.message, conn)
                if (currGreenBeans < (bags * 250)):
                    bags = math.floor(currGreenBeans/250)
                    beansToRoast = 250 * bags
                else:
                    beansToRoast = 250 * bags
                if(beansToRoast < 250):
                    await ctx.message.channel.send('You currently only have **' + f'{beansToRoast:,}' + '** grams of beans. You need at least 250 grams to make a bag.')
                else:
                    await ctx.message.channel.send('Using **' + f'{beansToRoast:,}' + '** grams of green beans to make **' + f'{bags:,}' + '** bags.')
                    roastMessage = await ctx.message.channel.send('Roasting')
                    if db.roast_beans_dark(ctx.message, beansToRoast, conn):
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='Roasting.')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='Roasting..')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='Roasting...')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Light] Roasting')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Light] Roasting.')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Light] Roasting..')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Light] Roasting...')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Medium] Roasting')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Medium] Roasting.')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Medium] Roasting..')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Medium] Roasting...')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Dark] Roasting')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Dark] Roasting.')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Dark] Roasting..')
                        await asyncio.sleep(1)
                        await roastMessage.edit(content='[Dark] Roasting...')
                        await asyncio.sleep(1)
                        beans = db.get_beans(ctx.message, conn)
                        await roastMessage.edit(content='Done! You have **' + f'{beans:,}' + '** grams of green beans remaining.')
                    else:
                        await ctx.message.channel.send('Something went wrong.')
        except ValueError:
            await ctx.message.channel.send('Please use a number. Example : ``$roast 2``')

    @client.command()
    async def sell(ctx, arg):
        bags = int(arg)
        db.check_user(ctx.message, conn)
        if(bags > 0):
            revenue = db.sell_bags(ctx.message, bags, conn)
            if(revenue >= 0):
                await ctx.message.channel.send('You earned **$' + f'{revenue:,}' + '**')
            else:
                await ctx.message.channel.send('You don\'t have any bags to sell.')
        else:
            await ctx.message.channel.send('You need to at least sell 1 bag!')
