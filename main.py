import os
import discord
import random
import sqlite3
from discord.ext import commands

TOKEN = 'MTAyMjc1MjY1NTk4ODIzMjIwMg.GhSFWq.a9HgpMQvFMfgCar8JFo7GJrJTGCSAjbOH3h_70'

#client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the F21 Discord server!'
    )
    
#@bot.event
#async def on_message(message):
#    print(message.author.id)
#    if message.author == bot.user:
#        return
#    
#    if "$" in message.content.lower():
#        print(message.content.lower())
#        content = message.content.lower()
#        content = content[1:].lower()
#        print(content)
#        if content == 'hello':
#            await message.channel.send('Hello!')
#        
#        if content == 'help':
#            await message.channel.send("Commands:\n$hello\n$help\n$ping")
#        
#        if content == 'ping':
#            await message.channel.send('Pong!')
#            
#    else:
#        pass
    
    
    
@bot.command(name='hello', help='Responds with a friendly greeting')

@bot.command(name="random", help="Responds with a random number between the two numbers you input")
async def rand(ctx, low: int, high: int):
        num = random.choice(range(low, high))
        await ctx.send('Your random number is: {}'.format(num))
        
@bot.command(name="add", help="Adds two numbers together")
async def add(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)
    
@bot.command(name="subtract", help="Subtracts two numbers")
async def subtract(ctx, num1: int, num2: int):
    await ctx.send(num1 - num2)
    


bot.run(TOKEN)