# bot.py
import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name="roll", help="Rolls any number of any sided dice, ex: 2d4")
async def roll(ctx, user_input):
    dice_array = user_input.split('d')
    result_array = [
        random.choice(range(1, int(dice_array[1]) + 1))
        for _ in range(int(dice_array[0]))
    ]
    await ctx.send(result_array)


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
    dice = [
        random.choice(range(1, 7))
        for _ in range(4)
    ]
    dice.remove(min(dice))
    stat_value = sum(dice)
    return stat_value


bot.run(TOKEN)
