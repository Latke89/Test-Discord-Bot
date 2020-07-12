# bot.py
import os
import discord
import random
import requests
import time
import datetime
from src.Models.Game_Mechanics.ConditionList import ConditionList
from src.Models.Game_Mechanics.Condition import Condition
from src.Cogs import Dice
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BASE_URL = os.getenv('BASE_URL')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
bot.load_extension('Cogs.Dice')

#
#


@bot.command(name='condition', help='Get a list of conditions, or specific condition')
async def get_condition(ctx, *args):
    if not args:
        conditions = []
        url = f'{BASE_URL}conditions/'
        print(url)
        resp = requests.get(url)
        if resp.status_code != 200:
            print(resp)
            print(f'GET {url} {resp.status_code}')
            await ctx.send('Unable to get list of conditions =\'(')
        else:
            print(resp.json())
            for item in resp.json()['results']:
                condition = ConditionList(item['index'], item['name'], item['url'])
                conditions.append(condition.name)
            condition_string = ', '.join(conditions)
            await ctx.send(f'List of conditions: {condition_string}')
    else:
        argument = args[0]
        url = f'{BASE_URL}conditions/{argument}'
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f'GET {url} {resp.status_code}')
            await ctx.send(f'Unable to get data for condition {argument}')
        else:
            json = resp.json()
            condition = Condition(json['_id'], json['index'], json['name'], json['desc'], json['url'])
            nl = '\n'
            await ctx.send(f'{condition.name}:\n{nl.join(condition.description)}')


@bot.listen()
async def on_command_error(ctx, error):
    print(error)
    await ctx.send('Unable to recognize that command')


@bot.event
async def on_message(message):
    timestamp = time.time()
    st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    with open('logs.txt', 'a') as text_file:
        print(f'<{st}> {message.author}: {message.content}', file=text_file)
    await bot.process_commands(message)


bot.run(TOKEN)
