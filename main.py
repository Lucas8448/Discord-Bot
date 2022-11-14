import os
import discord
import random
import sqlite3
from discord.ext import commands
import asyncio
import requests


# create database if not exists
if not os.path.exists('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    #create table that logs all messages
    c.execute('''CREATE TABLE user (name TEXT PRIMARY KEY, money INTEGER)''')
    #finish creating db
    conn.commit()
    conn.close()

#create message logger

#read token from token.txt
with open('token.txt', 'r') as f:
    TOKEN = f.read()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")  
    
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
    #filter explicit words
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
            
# money roleplay
@bot.command(name="work", description="Earn roleplay money")
async def work(ctx):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    if c.fetchone() is None:
        c.execute("INSERT INTO user VALUES (?, ?)", (ctx.author.name, 0))
        conn.commit()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    money = c.fetchone()[1]
    money += random.choice(range(1, 10))
    c.execute("UPDATE user SET money = ? WHERE name = ?", (money, ctx.author.name))
    conn.commit()
    await ctx.send(f"{ctx.author.name} earned money! They now have {money} dollars")
    conn.close()

@bot.command(name="money", description="View roleplay money")
async def money(ctx):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    if c.fetchone() is None:
        c.execute("INSERT INTO user VALUES (?, ?)", (ctx.author.name, 0))
        conn.commit()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    money = c.fetchone()[1]
    await ctx.send(f"{ctx.author.name} has {money} dollars")
    conn.close()
    
@bot.command(name="give", description="Give roleplay money to another user")
async def give(ctx):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    if c.fetchone() is None:
        c.execute("INSERT INTO user VALUES (?, ?)", (ctx.author.name, 0))
        conn.commit()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    money = c.fetchone()[1]
    if money >= 10:
        money -= 10
        c.execute("UPDATE user SET money = ? WHERE name = ?", (money, ctx.author.name))
        conn.commit()
        await ctx.send(f"{ctx.author.name} gave 10 dollars to {ctx.message.mentions[0].name}")
        c.execute("SELECT * FROM user WHERE name = ?", (ctx.message.mentions[0].name,))
        if c.fetchone() is None:
            c.execute("INSERT INTO user VALUES (?, ?)", (ctx.message.mentions[0].name, 0))
            conn.commit()
        c.execute("SELECT * FROM user WHERE name = ?", (ctx.message.mentions[0].name,))
        money2 = c.fetchone()[1]
        money2 += 10
        c.execute("UPDATE user SET money = ? WHERE name = ?", (money2, ctx.message.mentions[0].name))
        conn.commit()
    else:
        await ctx.send(f"{ctx.author.name} does not have enough money to give 10 dollars to {ctx.message.mentions[0].name}")
    conn.close()
    
@bot.command(name="rob", description="Rob roleplay money from another user")
async def rob(ctx):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    if c.fetchone() is None:
        c.execute("INSERT INTO user VALUES (?, ?)", (ctx.author.name, 0))
        conn.commit()
    c.execute("SELECT * FROM user WHERE name = ?", (ctx.author.name,))
    money = c.fetchone()[1]
    chance = random.choice(range(1, 10))
    if chance <= 5:
        money += random.choice(range(0, 100))
        c.execute("UPDATE user SET money = ? WHERE name = ?", (money, ctx.author.name))
        
        conn.commit()
        await ctx.send(f"{ctx.author.name} robbed {ctx.message.mentions[0].name} and got {money} dollars")
    else:
        await ctx.send(f"{ctx.author.name} failed to rob {ctx.message.mentions[0].name}")
    conn.close()
    
bot.run(TOKEN)
