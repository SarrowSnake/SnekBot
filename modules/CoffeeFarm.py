import asyncio
import discord
import time
import math
import Config as conf
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
    async def status(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await introMessage(ctx.message)
        else:
            userAvatar = ctx.author.avatar_url
            bags = db.get_bags(ctx.message, conn)
            beans = db.get_beans(ctx.message, conn)
            money = db.get_money(ctx.message, conn)
            trees = db.get_trees(ctx.message, conn)
            land = db.get_land(ctx.message, conn)
            outputString = f'**Money** : ${money:,.2f}' + '\n=====================\n' + f'**Green Beans** : {beans:,} grams.' + '\n' + f'**Bags** : {bags:,} bags.' + '\n' + f'**Trees** : {trees:,} trees.' + '\n' + f'**Land** : {land:,} acres.'

            statusEmbed = discord.Embed(title=ctx.author.display_name, description=outputString, colour=conf.colourCoffee)
            # Alternate
            """
            statusEmbed.add_field(name='Green Beans', value=f'{beans:,} grams.', inline=True)
            statusEmbed.add_field(name='Bags', value=f'{bags:,} bags.', inline=True)
            statusEmbed.add_field(name='Trees', value=f'{trees:,} trees.', inline=False)
            statusEmbed.add_field(name='Land', value=f'{land:,} acres.', inline=True)
            statusEmbed.add_field(name='Money', value=f'${money:,.2f}', inline=False)
            """
            statusEmbed.set_thumbnail(url=userAvatar)
            await ctx.message.channel.send(embed=statusEmbed)

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
            leaderEmbed = discord.Embed(title='Leaderboards - Top 10 Coffee Producer', description=outputString, colour=conf.colourCoffee)
            await ctx.message.channel.send(embed=leaderEmbed)
        elif(arg.lower() == 'money'):
            results = db.get_money_leaderboards(conn)
            outputString = ""
            for result in results:
                if(result[1] > 0):
                    name = result[0]
                    money = result[1]
                    outputString = f'{outputString}**{name}** with **${money:,.2f}**\n'
            leaderEmbed = discord.Embed(title='Leaderboards - Top 10 Wealthiest', description=outputString, colour=conf.colourCoffee)
            await ctx.message.channel.send(embed=leaderEmbed)
        else:
            outputString = 'Invalid option. Try adding ``beans`` or ``money`` at the end of the command.'
            leaderEmbed = discord.Embed(title='Can\'t Retrieve Leaderboards.', description=outputString, colour=conf.colourCoffee)
            await ctx.message.channel.send(embed=leaderEmbed)

    @client.command()
    async def prices(ctx):
        db.check_user(ctx.message, conn)
        results = db.get_last_prices(conn, 13)
        previousPrice = 0
        resultHistory = []
        outputString = ''

        for result in reversed(results):
            price = result[0]
            diff = float("{:.2f}".format(price - previousPrice))
            previousPrice = price
            resultHistory.append((price, diff))
        del resultHistory[0]
        count = 0
        for result in reversed(resultHistory):
            hisPrice = result[0]
            hisDiff = result[1]
            if hisDiff < 0:
                symbol = '\U0001F534'
                diff = '-$' + '{:.2f}'.format(abs(hisDiff))
                perc = '-{:.2f}%'.format(abs(hisDiff/hisPrice))
            elif result[1] > 0:
                symbol = '\U0001F7E2'
                diff = '+$' + '{:.2f}'.format(abs(hisDiff))
                perc = '+{:.2f}%'.format(abs(hisDiff/hisPrice))
            else:
                symbol = '\U000026AA'
                diff = '$0.00'
            hisPrice = '{:.2f}'.format(float(hisPrice))
            outputString = f'{outputString}[{symbol} {perc}] **${hisPrice}** {diff} '
            if count < 1:
                outputString = f'{outputString} | **CURRENT**\n'
                count += 30
            else:
                if(count < 60):
                    outputString = f'{outputString} | {count%60} minutes ago.\n'
                elif(count % 60 == 0):
                    outputString = f'{outputString} | {int(math.floor(count/60))} hours ago.\n'
                else:
                    outputString = f'{outputString} | {int(math.floor(count/60))} hours and {count%60} minutes ago.\n'
                count += 30
        pricesEmbed = discord.Embed(title='Coffee Price History', description=outputString, colour=conf.colourCoffee)
        nextTickTime = 1800 - int(math.floor(time.time() % 1800))
        footerText = ''
        if(nextTickTime > 60):
            footerText = f'{footerText}Next tick : {int(math.floor(nextTickTime/60))} minutes and {int(math.floor(nextTickTime%60))} seconds.\n'
        else:
            footerText = f'{footerText}Next tick : {int(math.floor(nextTickTime%60))} seconds.\n'
        footerText = f'{footerText}Prices are updated every 30 minutes.'
        pricesEmbed.set_footer(text=footerText)
        await ctx.message.channel.send(embed=pricesEmbed)

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
            outputString = 'Your coffee tree have been planted! Please wait a while until it\'s ready to harvest.'
            plantEmbed = discord.Embed(title='Coffee has been Planted!', description=outputString, colour=conf.colourCoffee)
            await ctx.message.channel.send(embed=plantEmbed)
        else:
            outputString = 'You\'ve already planted a tree!'
            plantEmbed = discord.Embed(title='Coffee Already Planted!', description=outputString, colour=conf.colourCoffee)
            await ctx.message.channel.send(embed=plantEmbed)

    @client.command()
    async def harvest(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await introMessage(ctx.message)
        else:
            harvestedBeans = db.harvest_beans(ctx.message, conn)
            if(harvestedBeans >= 0):
                outputString = 'You harvested your coffee trees and got **' + f'{harvestedBeans:,}' + '** grams of green beans!'
                harvestEmbed = discord.Embed(title='Coffee Harvested!', description=outputString, colour=conf.colourCoffee)
                await ctx.message.channel.send(embed=harvestEmbed)
            else:
                outputString = 'You haven\'t ``$plant``ed any trees yet! .'
                harvestEmbed = discord.Embed(title='No Coffee to Harvest!', description=outputString, colour=conf.colourCoffee)
                await ctx.message.channel.send(embed=harvestEmbed)

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
                    if db.roast_beans(ctx.message, beansToRoast, conn):
                        beans = db.get_beans(ctx.message, conn)
                        outputString = f'Done! You\'ve used **{beansToRoast:,}** beans to make **{bags:,}** bags. You have **{beans:,}** grams of green beans remaining.'
                        roastEmbed = discord.Embed(title='Beans Roasted!', description=outputString, colour=conf.colourCoffee)
                        await ctx.message.channel.send(embed=roastEmbed)
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
                outputString = f'You\'ve earned **${revenue:,.2f}** from selling **{bags:,}** bags.'
                sellEmbed = discord.Embed(title='Coffee Sold!', description=outputString, colour=conf.colourCoffee)
                await ctx.message.channel.send(embed=sellEmbed)
            else:
                outputString = f'You don\'t have any bags to sell. Try roasting your green beans by doing ``$roast [# of bags]``!'
                sellEmbed = discord.Embed(title='No Bags!', description=outputString, colour=conf.colourCoffee)
                await ctx.message.channel.send(embed=sellEmbed)
        else:
            outputString = f'You need to sell at least 1 bag!'
            sellEmbed = discord.Embed(title='Invalid Bag Ammount.', description=outputString, colour=conf.colourCoffee)
            await ctx.message.channel.send(embed=sellEmbed)
