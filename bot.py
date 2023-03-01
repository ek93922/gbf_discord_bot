from discord.ext import commands
from datetime import datetime
import math
import discord
import gbf_wiki


# Token needs str
BOT_TOKEN = 

# Channel ID must be int
CHANNEL_ID = 

bot = commands.Bot(command_prefix= "!", intents= discord.Intents.all())

@bot.event
async def on_ready():
    channel= bot.get_channel(CHANNEL_ID)
    # await - function waits for this line to finish before moving on 
    await channel.send("Hello! Zooey-Bot is ready.")

@bot.command()
# Takes in context argument
async def hello(ctx):
    await ctx.send("Hello.")

# @bot.command()
# async def add(ctx, x, y):
#     result = int(x) + int(y)
#     await ctx.send(f'{x} + {y} = {result}')

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i) 

    await ctx.send(f'>>> Result = {result}')

@bot.command()
async def test(ctx):
    await ctx.send('>>> Testing ```testing```')

@bot.command()
async def current(ctx):
    speech = gbf_wiki.GbfWiki.cur_event()
    
    await ctx.send(speech)

@bot.command()
async def upcoming(ctx):
    speech = gbf_wiki.GbfWiki.up_event()

    await ctx.send(speech)

@bot.command()
async def search(ctx, *, arg):
    speech = gbf_wiki.GbfWiki.search(arg)
    
    await ctx.send(speech)


bot.run(BOT_TOKEN)