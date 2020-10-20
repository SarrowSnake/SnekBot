import asyncio
import discord
import random
import Config as conf
from discord.utils import get

busy = False
prefix = conf.prefix

def BaseCommands(client):

    global busy

    ''' Essential commands '''
    @client.command()
    async def about(ctx):
        botAvatar = client.user.avatar_url
        aboutMessage = f'Version : **{conf.botVersion}**'
        aboutEmbed = discord.Embed(title='About SnekBot', description=aboutMessage, colour=conf.colourGeneral)
        aboutEmbed.set_thumbnail(botAvatar)
        await ctx.message.channel.send(embed=aboutEmbed)

    async def help(ctx, arg: str=None):
        #initialize help message Variable
        helpMessage = ''
        helpTitle = 'Help'
        commandsArray = []
        helpColour = conf.colourGeneral
        if arg is None:
            #Print all basic commands here
            #String template : f'``{conf.prefix}name`` : description.'
            commandsArray.append(f'``{conf.prefix}notifyme`` : Add/Remove the Updates role to yourself. Use this to get notified for future server/bot updates.')
            commandsArray.append(f'``{conf.prefix}ilovecoffee`` : Add/Remove the Coffee Nerd role to yourself.')
            commandsArray.append(f'``{conf.prefix}pronoun [name]`` : Add/Remove a pronoun role. use ``$pronoun`` to show a list of available pronouns.')
            commandsArray.append(f'``{conf.prefix}equipment [name]`` : Add/Remove a role to show which coffee equipment you\'re using!')
            commandsArray.append(f'``{conf.prefix}ctof [#]``/``{conf.prefix}ftoc [#]`` : Converts °C to °F or °F to °C.')
            commandsArray.append(f'``{conf.prefix}facts`` : Have me tell you about a random coffee fact!')
            commandsArray.append(f'``{conf.prefix}brew`` : Let me brew you a cup of coffee!')
            for cmdRow in commandsArray:
                helpMessage = f'{helpMessage}{cmdRow}\n'
            helpMessage = f'{helpMessage}\nUse ``$help coffee`` for all Coffee Farming commands.'
        elif arg.lower() == 'coffee':
            #Print all coffee game commands here
            helpTitle = f'{helpTitle} - Coffee Farming'
            helpColour = conf.colourCoffee
            commandsArray.append(f'``{conf.prefix}tutorial`` : Coming Soon!')
            commandsArray.append(f'``{conf.prefix}status`` : Show your current player status.')
            commandsArray.append(f'``{conf.prefix}leaderboards [beans/money]`` : Shows current available leaderboards.')
            commandsArray.append(f'``{conf.prefix}prices`` : Shows current selling price for bags of coffee.')
            commandsArray.append(f'``{conf.prefix}plant`` : Starts planting owned coffee trees!')
            commandsArray.append(f'``{conf.prefix}harvest`` : Harvests all coffee tress.')
            commandsArray.append(f'``{conf.prefix}roast [# of bags]`` : Roasts coffee beans and turns them into coffee bags! (250gr of coffee each)')
            commandsArray.append(f'``{conf.prefix}sell [# of bags]`` : Sells specified number of coffee bags.')
            for cmdRow in commandsArray:
                helpMessage = f'{helpMessage}{cmdRow}\n'
            helpMessage = f'{helpMessage}\nAll commands might be subject to change, behavior wise.'
        else:
            #Print error message here
            helpTitle = f'{helpTitle} - Error'
            helpColour = conf.colourSerious
            helpMessage = f'Invalid argument. Try ``{conf.prefix}help`` or ``{conf.prefix}help coffee`` instead.'
        helpEmbed = discord.Embed(title=helpTitle, description=helpMessage, colour=helpColour)
        await ctx.message.channel.send(embed=helpEmbed)


    @client.command()
    async def shutdown(ctx):
        if ctx.message.author.id == conf.ownerId:
            botAvatar = client.user.avatar_url
            shutdownEmbed = discord.Embed(title='Goodbye!', description='Shutting down...', colour=conf.colourSerious)
            shutdownEmbed.set_thumbnail(url=botAvatar)
            await ctx.message.channel.send(embed=shutdownEmbed)
            await client.change_presence(status=discord.Status.offline)
            exit()
        else:
            await ctx.message.channel.send('You are not authorized to use this command.')

    @client.command()
    async def notifyme(ctx, *, arg: str=None):
        rolesList = ['Updates', 'Game Night'];
        stringRoleGiven = 'You now have the {} role!'
        if arg is None:
            stringRole = 'List of available roles :\n'
            for role in rolesList:
                stringRole = f'{stringRole}{role}\n'
                roleEmbed = discord.Embed(title='Obtainable Roles', description=stringRole, colour=conf.colourGeneral)
            await ctx.message.channel.send(embed=roleEmbed)
        else:
            for role in rolesList:
                if arg.lower() == role.lower():
                    if get(ctx.author.roles, name=role):
                        await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=role), reason='Role removed by user via bot command.')
                        roleEmbed = discord.Embed(title='Role Removed!', description=f'You are now opted out of {role}.', colour=conf.colourGeneral)
                    else:
                        await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name=role), reason='Role requested from user via bot command.')
                        roleEmbed = discord.Embed(title='Role Given!', description=f'You are now notified for {role}!', colour=conf.colourGeneral)
                    break
                else:
                    stringRoleNotFound = 'Your requested equipment role is not found. Try using the command without any arguments (example : ``$notifyme``) for a list of available obtainable roles.'
                    roleEmbed = discord.Embed(title='Role Not Found!', description=stringRoleNotFound, colour=conf.colourSerious)
            await ctx.message.channel.send(embed=roleEmbed)

    # Role Assigments
    @client.command()
    async def ilovecoffee(ctx):
        await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name='Coffee Nerd'), reason='Role requested from user via bot command.')
        roleEmbed = discord.Embed(title='Role Given!', description='You now have the Coffee Nerd role!', colour=conf.colourGeneral)
        await ctx.message.channel.send(embed=roleEmbed)

    @client.command()
    async def pronoun(ctx, arg: str=None):
        stringRoleGiven = "You now identify as {}!"
        stringMaleRole = 'He/Him'
        stringFemaleRole = 'She/Her'
        stringNBRole = 'They/Them'
        if arg is None:
            #Print obtainable roles
            pronounsList = f'He/Him\nShe/Her\nThey/Them'
            roleEmbed = discord.Embed(title='Available Pronouns', description=pronounsList, colour=conf.colourGeneral)
            await ctx.message.channel.send(embed=roleEmbed)
        else:
            if arg.lower() == "he" or arg.lower() == "him" or arg.lower() == "he/him":
                if get(ctx.author.roles, name='He/Him'):
                    await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=stringMaleRole), reason='Role removed by user via bot command.')
                    roleEmbed = discord.Embed(title='Role Removed!', description='', colour=conf.colourGeneral)
                    await ctx.message.channel.send(embed=roleEmbed)
                else:
                    await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name=stringMaleRole), reason='Role requested from user via bot command.')
                    roleEmbed = discord.Embed(title='Role Given!', description=stringRoleGiven.format(stringMaleRole), colour=conf.colourGeneral)
                    await ctx.message.channel.send(embed=roleEmbed)
            if arg.lower() == "she" or arg.lower() == "her" or arg.lower() == "she/her":
                if get(ctx.author.roles, name='She/Her'):
                    await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=stringFemaleRole), reason='Role removed by user via bot command.')
                    roleEmbed = discord.Embed(title='Role Removed!', description='', colour=conf.colourGeneral)
                    await ctx.message.channel.send(embed=roleEmbed)
                else:
                    await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name=stringFemaleRole), reason='Role requested from user via bot command.')
                    roleEmbed = discord.Embed(title='Role Given!', description=stringRoleGiven.format(stringFemaleRole), colour=conf.colourGeneral)
                    await ctx.message.channel.send(embed=roleEmbed)
            if arg.lower() == "they" or arg.lower() == "them" or arg.lower() == "they/them":
                if get(ctx.author.roles, name='They/Them'):
                    await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=stringNBRole), reason='Role removed by user via bot command.')
                    roleEmbed = discord.Embed(title='Role Removed!', description='', colour=conf.colourGeneral)
                    await ctx.message.channel.send(embed=roleEmbed)
                else:
                    await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name=stringNBRole), reason='Role requested from user via bot command.')
                    roleEmbed = discord.Embed(title='Role Given!', description=stringRoleGiven.format(stringNBRole), colour=conf.colourGeneral)
                    await ctx.message.channel.send(embed=roleEmbed)

    @client.command()
    async def equipment(ctx, *, arg: str=None):
        equipmentList = ['Cold Brew', 'French Press', 'AeroPress', 'Melitta', 'Chemex', 'V60', 'Moka Pot', 'Keurig', 'Manual Espresso', 'Super-Automatic', 'Semi-Automatic']
        stringRoleGiven = 'You now have the {} role!'
        if arg is None:
            stringEquipments = 'List of available equipment roles :\n'
            for eq in equipmentList:
                stringEquipments = f'{stringEquipments}{eq}\n'
                equipmentEmbed = discord.Embed(title='Equipment Roles', description=stringEquipments, colour=conf.colourGeneral)
                equipmentEmbed.set_footer(text='\"$equipment clear\" to clear all equipment roles.')
            await ctx.message.channel.send(embed=equipmentEmbed)
        elif arg.lower() == 'clear':
            clearingEmbed = discord.Embed(title='Clearing All Equipment Roles...', description='Please wait.', colour=conf.colourGeneral)
            equipmentClearMessage = await ctx.message.channel.send(embed=clearingEmbed)
            for eq in equipmentList:
                await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=eq), reason='Role removed by user via bot command.')
            stringEquipments = 'All equipment roles have been removed!'
            equipmentEmbed = discord.Embed(title='Removed All Equipment Roles!', description=stringEquipments, colour=conf.colourGeneral)
            await equipmentClearMessage.edit(embed=equipmentEmbed)
        else:
            arg = arg.lower()
            if arg == 'manual':
                arg = 'manual espresso'
            if arg == 'super' or arg =='auto':
                arg = 'super-automatic'
            if arg == 'semi':
                arg = 'semi-automatic'
            for eq in equipmentList:
                if arg == eq.lower():
                    if get(ctx.author.roles, name=eq):
                        await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=eq), reason='Role removed by user via bot command.')
                        equipmentEmbed = discord.Embed(title='Equipment Role Removed!', description=f'The {eq} role has been removed!', colour=conf.colourGeneral)
                    else:
                        await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name=eq), reason='Role requested from user via bot command.')
                        equipmentEmbed = discord.Embed(title='Equipment Role Given!', description=stringRoleGiven.format(eq), colour=conf.colourGeneral)
                    break
                else:
                    stringRoleNotFound = 'Your requested equipment role is not found. Try using the command without any arguments (example : ``$equipment``) for a list of available obtainable equipments.'
                    equipmentEmbed = discord.Embed(title='Equipment Role Not Found!', description=stringRoleNotFound, colour=conf.colourSerious)
            await ctx.message.channel.send(embed=equipmentEmbed)

        ''' Non-Essential commands '''

    @client.command()
    async def say(ctx, *, msg):
        if ctx.author.id == conf.ownerId:
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
        if not(busy):
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
    async def ctof(ctx, arg: float=None):
        if arg != None:
            output = (9/5)*arg + 32
            ctofEmbed = discord.Embed(title='C to F Conversion', description=f'{arg:.1f}°C is **{output:.1f}**°F', colour=conf.colourGeneral)
        else:
            ctofEmbed = discord.Embed(title='C to F Conversion', description='Please enter a number.', colour=conf.colourSerious)
        await ctx.message.channel.send(embed=ctofEmbed)

    @client.command()
    async def ftoc(ctx, arg: float=None):
        if arg != None:
            output = (arg-32)*5/9
            ctofEmbed = discord.Embed(title='F to C Conversion', description=f'{arg:.1f}°F is **{output:.1f}**°C', colour=conf.colourGeneral)
        else:
            ctofEmbed = discord.Embed(title='F to C Conversion', description='Please enter a number.', colour=conf.colourSerious)
        await ctx.message.channel.send(embed=ctofEmbed)

    @client.command()
    async def oztog(ctx, arg: float=None):
        if arg != None:
            output = arg * 28.34952
            oztogEmbed = discord.Embed(title='Ounces to Grams Conversion', description=f'{arg:.2f} ounces is **{output:.2f}** grams.', colour=conf.colourGeneral)
        else:
            oztogEmbed = discord.Embed(title='Ounces to Grams Conversion', description=f'Please enter a number.', colour=conf.colourSerious)
        await ctx.message.channel.send(embed=oztogEmbed)

    @client.command()
    async def gtooz(ctx, arg: float=None):
        if arg != None:
            output = arg / 28.34952
            gtoozEmbed = discord.Embed(title='Ounces to Grams Conversion', description=f'{arg:.2f} grams is **{output:.2f}** ounces.', colour=conf.colourGeneral)
        else:
            gtoozEmbed = discord.Embed(title='Ounces to Grams Conversion', description=f'Please enter a number.', colour=conf.colourSerious)
        await ctx.message.channel.send(embed=gtoozEmbed)

    @client.command()
    async def countdown(ctx):
        global busy
        if not(busy):
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

    @client.command()
    async def getavatar(ctx, arg: discord.User=None):
        if arg is None:
            await ctx.message.channel.send(ctx.message.author.avatar_url_as(format='png'))
        else:
            await ctx.message.channel.send(arg.avatar_url_as(format='png'))
