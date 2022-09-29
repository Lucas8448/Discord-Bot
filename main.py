from binascii import crc_hqx
from http import client
import os
import discord
import random
import sqlite3
from discord.ext import commands
import asyncio
import requests

TOKEN = 'MTAyMjc1MjY1NTk4ODIzMjIwMg.GhSFWq.a9HgpMQvFMfgCar8JFo7GJrJTGCSAjbOH3h_70'


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# delete tenor messages in all channels other than memes


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the F21 Discord server!'
    )


@bot.command(name="random", help="Responds with a random number between the two numbers you input")
async def rand(ctx, low: int, high: int):
    num = random.choice(range(low, high))
    await ctx.send('Your random number is: {}'.format(num))


@bot.command(name="dice", help="Rolls a dice")
async def roll(ctx):
    await ctx.send('Rolling the dice...')
    await ctx.send('You rolled a {}'.format(random.choice(range(1, 6))))


@bot.command(name="vcmute", help="Times out a user for a specified amount of time")
async def timeout(ctx, user: discord.Member, time: int):
    # check if user is moderator or lærer
    role = discord.utils.get(ctx.guild.roles, name="Moderator")
    role2 = discord.utils.get(ctx.guild.roles, name="Lærer")
    if role in ctx.author.roles or role2 in ctx.author.roles:
        await ctx.send(f'{user.mention} has been muted for {time} seconds')
        await user.edit(mute=True)
        await asyncio.sleep(time)
        await user.edit(mute=False)
        await ctx.send(f'{user.mention} has been unmuted')
    else:
        await ctx.send('You do not have the permissions to do this')


@bot.command(name="wikipedia", help="Searches wikipedia for a specified topic")
async def wiki(ctx, *, search):
    await ctx.send('Searching wikipedia for {}'.format(search))
    search = search.replace(" ", "_")
    await ctx.send('https://en.wikipedia.org/wiki/{}'.format(search))


@bot.command(name="commands")
async def commands(ctx):
    await ctx.send("Commands:\n!random [low] [high]\n!dice\n!wikipedia [search]")


@bot.command(name="dm", help="Sends a DM to a user")
async def dm(ctx, user: discord.Member, *, message):
    if message.channel.type == discord.ChannelType.private:
        if message.author.id == 977654996998975489:
            await user.create_dm()
            await user.dm_channel.send(message)
            await ctx.send(f'DM sent to {user}')
    else:
        role = discord.utils.get(ctx.guild.roles, name="Moderator")
        role2 = discord.utils.get(ctx.guild.roles, name="Lærer")
        if role in ctx.author.roles or role2 in ctx.author.roles:
            await user.create_dm()
            await user.dm_channel.send(message)
            await ctx.send(f'DM sent to {user}')
        else:
            await ctx.send('You do not have the permissions to do this')


@bot.command(name="p", description="send a web request to a website and prints the time used for the request")
async def ping(ctx, *, website):
    c = requests.get("https://" + website)
    await ctx.send("Website: " + website + "\nResponse time: " + str(c.elapsed.total_seconds()) + " seconds")

# bot voice chat functions

# join users voice channel


@bot.command(name="join", description="Make bot join voice channel")
async def joinvc(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except Exception as e:
        print(e)
        await ctx.send(f"Could not connect to voice channel")

# leave voice channel


@bot.command(name="leave", description="Leave voice channel")
async def leavevc(ctx):
    try:
        await ctx.voice_client.disconnect()
    except Exception as e:
        print(e)
        await ctx.send(f"Could not leave voice channel")

# meme filter


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name == "memes" or message.channel.name == "off-topic":
        await bot.process_commands(message)
    else:
        if "tenor" in message.content:
            await message.delete()
        else:
            await bot.process_commands(message)


bot.run(TOKEN)
