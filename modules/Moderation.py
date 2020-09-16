import asyncio
import discord
import typing
import Config as conf
from discord.ext import commands
from discord.utils import get
from utils import DatabaseController as db


busy = False

def ownerCheck(author):
    if (author.id == conf.ownerId):
        return True
    else:
        return False

def moderatorCheck(author):
    if (get(author.roles, name='Moderator')  or (author.id == conf.ownerId)):
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
            embedMessage = f'**{arg}** messages have been deleted by **{ctx.author.name}**.'
            purgeEmbed = discord.Embed(title='Messages Deleted', description=embedMessage, colour=conf.colourModeration)
            await ctx.message.channel.send(embed=purgeEmbed)
        else:
            embedMessage = 'You do not have access to this command.'
            purgeEmbed = discord.Embed(title='Access Denied', description=embedMessage, colour=conf.colourSerious)
            await ctx.message.channel.send(embed=purgeEmbed)

    @purge.error
    async def info_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send('Something went wrong.')
            print('Argument type error.')
