import asyncio
import discord
import random
import Config as conf

busy = False
prefix = conf.prefix

def BaseCommands(client):

    global busy

    ''' Essential commands '''

    @client.command()
    async def shutdown(ctx):
        if str(ctx.message.author.id) == conf.ownerId:
            await ctx.message.channel.send('Shutting down. Goodbye!')
            await client.change_presence(status=discord.Status.offline)
            exit()
        else:
            await ctx.message.channel.send('You are not authorized to use this command.')

    ''' Note self : ilovecoffee command should be moved to actual moderator modules '''
    @client.command()
    async def ilovecoffee(ctx):
        await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name='Coffee Nerd'), reason='Role requested from user via bot command.')
        roleEmbed = discord.Embed(title='Role Given!', description='You now have the Coffee Nerd role!', colour=0x005064)
        await ctx.message.channel.send(embed=roleEmbed)

        ''' Non-Essential commands '''

    @client.command()
    async def say(ctx, *, msg):
        if str(ctx.author.id) == conf.ownerId:
            await ctx.message.delete()
            async with ctx.channel.typing():
                await asyncio.sleep(3)
            await ctx.send(msg)
        else:
            await ctx.send('You are not authorized to use this command.')

    @client.command()
    async def hello(ctx):
        async with ctx.message.channel.typing():
            await asyncio.sleep(3)
        await ctx.message.channel.send('Hello, ' + ctx.message.author.mention + '!')

    @client.command()
    async def ping(ctx):
        await ctx.message.channel.send('Pong!')

    @client.command()
    async def facts(ctx):
        async with ctx.message.channel.typing():
            await asyncio.sleep(5)
        with open('coffeefacts.txt') as f:
            lines = f.readlines()
        await ctx.message.channel.send(random.choice(lines))

    @client.command()
    async def brew(ctx):
        randNum = random.randint(0, 14)
        brewMessage = await ctx.message.channel.send('Brewing')
        await asyncio.sleep(1)
        await brewMessage.edit(content='Brewing.')
        await asyncio.sleep(1)
        await brewMessage.edit(content='Brewing..')
        await asyncio.sleep(1)
        await brewMessage.edit(content='Brewing...')
        await asyncio.sleep(1)
        if randNum != 7:
            await brewMessage.edit(content=':coffee: Here you go!')
        else:
            await brewMessage.edit(content=':tea: Here you go! ...wait')
            await asyncio.sleep(5)
            await brewMessage.edit(content=':coffee: Here you go! Sorry about that :broken_heart:')

    @client.command()
    async def boop(ctx):
        await ctx.message.channel.send('<:googleseviper:745643309669548133>:purple_heart:')

    @client.command()
    async def boom(ctx):
        global busy
        if(busy == False):
            busy = True
            await ctx.message.channel.send(':boom:')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Why did you do that, ' + ctx.message.author.mention + '?')
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Going down for repairs. :(')
            await asyncio.sleep(3)
            await client.change_presence(status=discord.Status.offline)
            await asyncio.sleep(12)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prefix+'help'))
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send('Don\'t do that again please :broken_heart:')
            busy = False

    @client.command()
    async def countdown(ctx):
        global busy
        if(busy == False):
            busy = True
            countdownMessage = await ctx.message.channel.send('3')
            await asyncio.sleep(1)
            await countdownMessage.edit(content='2')
            await asyncio.sleep(1)
            await countdownMessage.edit(content='1')
            await asyncio.sleep(1)
            await countdownMessage.edit(content=':checkered_flag:')
            busy = False
            await asyncio.sleep(15)
            await countdownMessage.edit(content='Countdown finished.')
