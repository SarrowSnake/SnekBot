import discord
from utils import DatabaseController as db
import modules.CoffeeFarm as cf
import Config as conf

# Shop Notes
# 1 Acre = 500 plants
# 1 Plant = 2000 grams
# Yield time = 18 Hours

def CoffeeShop(client, conn):

    global db

    @client.command()
    async def shop(ctx):
        db.check_user(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            await cf.introMessage(ctx.message)
        else:
            itemTrees = f'Trees : **$10** per tree.'
            itemLand = f'Land : **$5,000** per acre (space for 500 trees).'
            outputString = itemTrees + '\n' + itemLand
            shopEmbed = discord.Embed(title='Shop', description=outputString, colour=conf.colourCoffee)
            footerString = '$buy [item name] [amount]'
            tempString = footerString + '\nWORK IN PROGRESS. DO NOT USE.'
            shopEmbed.set_footer(text=tempString)
            await ctx.message.channel.send(embed=shopEmbed)

    @client.command()
    async def buy(ctx, item: str, amount: int):
        db.check_user(ctx.message, conn)
        item = item.lower()
        currentMoney = db.get_money(ctx.message, conn)
        if not(db.check_player(ctx.message, conn)):
            cf.introMessage(ctx.message)
        else:
            if item == 'trees':
                availableAcres = db.get_land(ctx.message, conn)
                currentTrees = db.get_trees(ctx.message, conn)
                maxTreesLimit = conf.treesLimit * availableAcres
                # Check if trees have been planted
                if db.get_plant_status(ctx.message, conn) is True:
                    outputString = f'You currently have not harvested your trees yet! You\'re allowed to buy more trees after you\'ve harvested your coffee beans.'
                    buyEmbed = discord.Embed(title='Shop - Unharvested Crops', description=outputString, colour=conf.colourCoffee)
                    await ctx.message.channel.send(embed=buyEmbed)
                # Check if the amount of trees you're buying are exceeding the limit
                elif (currentTrees + amount) > maxTreesLimit:
                    outputString = f'You have no more room for more trees! Currently you only have **{(maxTreesLimit - currentTrees):,}** trees worth of free space. Buy more land to plant more trees!'
                    buyEmbed = discord.Embed(title='Shop - Insufficient Room', description=outputString, colour=conf.colourCoffee)
                    await ctx.message.channel.send(embed=buyEmbed)
                # Check if the player has enough money to purchase the trees
                elif currentMoney < (amount * conf.treePrice):
                    outputString = f'You currently have **${currentMoney:,.2f}** and tried to buy **${(amount*conf.treePrice):,.2f}** worth of {item}. Sell bags of coffee to get more money!'
                    buyEmbed = discord.Embed(title='Shop - Insufficient Funds', description=outputString, colour=conf.colourCoffee)
                    await ctx.message.channel.send(embed=buyEmbed)
                else:
                    db.buy_trees(ctx.message, amount, conn)
                    outputString = f'You\'ve bought {amount} {item}!'
                    buyEmbed = discord.Embed(title='Shop - Purchase Successful!', description=outputString, colour=conf.colourCoffee)
                    await ctx.message.channel.send(embed=buyEmbed)
            if item == 'land':
                # Check if the player has enough money to buy the land
                if currentMoney < (amount * conf.landPrice):
                    outputString = f'You currently have **${currentMoney:,.2f}** and tried to buy **${(amount*conf.landPrice):,.2f}** worth of {item}. Sell bags of coffee to get more money!'
                    buyEmbed = discord.Embed(title='Shop - Insufficient Funds', description=outputString, colour=conf.colourCoffee)
                    await ctx.message.channel.send(embed=buyEmbed)
                else:
                    db.buy_land(ctx.message, amount, conn)
                    outputString = f'You\'ve bought {amount} {item}!'
                    buyEmbed = discord.Embed(title='Shop - Purchase Successful!', description=outputString, colour=conf.colourCoffee)
                    await ctx.message.channel.send(embed=buyEmbed)
