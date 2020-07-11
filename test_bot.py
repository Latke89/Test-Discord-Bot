# bot.py
import os
import discord
import random
import requests
import time
import datetime
from Models.Game_Mechanics.ConditionList import ConditionList
from Models.Game_Mechanics.Condition import Condition
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BASE_URL = os.getenv('BASE_URL')

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.command(name="roll", help="Simulates rolling dice ex: 2d4, 1d8 + 5")
async def roll(ctx, *, arg):
    # If roll has a modifier
    if "+" in arg or "-" in arg:
        components = arg.split(' ')
        dice_array = components[0].split('d')
        modifier = int(components[2])
        operand = components[1]

        # Get array of numbers based on user input, aka rolling dice
        result_array = [
            random.choice(range(1, int(dice_array[1]) + 1))
            for _ in range(int(dice_array[0]))
        ]
        if operand == '+':
            await ctx.send(f'Result: {result_array} + {modifier}\n'
                           f'Sum of dice: {sum(result_array) + modifier}')
        else:
            await ctx.send(f'Result: {result_array} - {modifier}\n'
                           f'Sum of dice: {sum(result_array) - modifier}')
    else:
        dice_array = arg.split('d')
        result_array = [
            random.choice(range(1, int(dice_array[1]) + 1))
            for _ in range(int(dice_array[0]))
        ]
        await ctx.send(f'Result: {result_array}\nSum of dice: {sum(result_array)}')


@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        ctx.send('Please check your formatting and query')


@bot.command(name='roll_stats', help='Rolls initial player stats')
async def roll_stats(ctx, times_called=0):
    stat_array = []
    for _ in range(7):
        stat_array.append(_roll_single_stat())
    stat_array.remove(min(stat_array))
    if sum(stat_array) >= 70:
        await ctx.send(stat_array)
    else:
        times_called += 1
        print(f"roll_stats has been called {times_called} times with stat_array {stat_array}")
        await ctx.send(f"Sum of {stat_array} is less than 70, rerolling stats...")
        await roll_stats(ctx, times_called)


def _roll_single_stat():
    # Rolling 4 six sided dice, and dropping the lowest result
    dice = [
        random.choice(range(1, 7))
        for _ in range(4)
    ]
    dice.remove(min(dice))
    stat_value = sum(dice)
    return stat_value


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
