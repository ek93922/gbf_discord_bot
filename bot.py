from discord.ext import commands
from datetime import datetime
import math
import discord
import gbf_wiki



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

    cur_evt_list, start_time, end_time, timestamp = gbf_wiki.GbfWiki.cur_event()
    
    speech = '>>> Current Events\n--------------------------------------\n'
    
    # For showing current events. Check if the event has started or will start soon.
    # Use current dynamic timestamp and subtract start dynamic timestamp
    # If the value is - then it started, if the value is + then it will start soon.
    i = 0
    while i < len(cur_evt_list):
        delta = timestamp - int(start_time[i])
        ts1 = datetime.fromtimestamp(timestamp)

        if delta < 0:
            ts2 = datetime.fromtimestamp(int(start_time[i]))
            delta = ts2 - ts1
            d = int(delta.days)
            h = math.trunc(delta.seconds/3600)
            if d < 1:
                speech += (f'**{cur_evt_list[i]}** starts in {h}h (<t:{start_time[i]}:f>)\n')
            else:    
                speech += (f'**{cur_evt_list[i]}** starts in {d}d {h}h (<t:{start_time[i]}:f>)\n')
        else:
            ts2 = datetime.fromtimestamp(int(end_time[i]))
            delta = ts2 - ts1
            d = delta.days
            h = math.trunc(delta.seconds/3600)
            if d < 1:
                speech += (f'**{cur_evt_list[i]}** will end in {h}h (<t:{end_time[i]}:f>)\n')
            else:
                speech += (f'**{cur_evt_list[i]}** will end in {d}d {h}h (<t:{end_time[i]}:f>)\n')
        i += 1

    
    await ctx.send(speech)

@bot.command()
async def upcoming(ctx):
    speech = '''>>> Upcoming Events\n--------------------------------------\n'''
    up_event = gbf_wiki.GbfWiki.up_event()
    for event in up_event:
        start_date = up_event[event][0]
        speech += f'**{event}** starts on <t:{start_date}>\n'

    await ctx.send(speech)

@bot.command()
async def search(ctx, *, arg):
    speech = gbf_wiki.GbfWiki.search(arg)
    await ctx.send(speech)


bot.run(BOT_TOKEN)