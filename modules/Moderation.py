import asyncio
import discord
import typing
import Config as cf
from discord.ext import commands
from discord.utils import get
from utils import DatabaseController as db


busy = False

def moderatorCheck(author):
    if (get(author.roles, name='Moderator')  or (author.id == cf.ownerId)):
        return True
    else:
        return False

def Moderation(client, conn):

    global busy
    global db

    @client.command()
    async def purge(ctx, arg: int):
        if(moderatorCheck(ctx.author)):
            channelMessages = await ctx.message.channel.history(limit=arg+1).flatten()
            await ctx.message.channel.delete_messages(channelMessages)
            embedMessage = '**' + str(arg) + '** messages have been deleted by **' + ctx.author.name + '**.'
            modEmbed = discord.Embed(title='Messages Deleted', description=embedMessage, colour=0x005064)
            await ctx.message.channel.send(embed=modEmbed)
        else:
            await ctx.message.channel.send('You do not have access to this command.')

    @purge.error
    async def info_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send('Something went wrong.')
            print('Argument type error.')
