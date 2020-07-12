import discord
import random
from discord.ext import commands


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def roll(self, ctx, *, arg):
        """Simulates rolling dice ex: 2d4, 1d8 + 5"""
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

    # @roll.error
    # async def roll_error(self, ctx, error):
    #     if isinstance(error, commands.BadArgument):
    #         ctx.send('Please check your formatting and query')

    @commands.command(name='roll_stats', alias='stats')
    async def roll_stats(self, ctx, times_called=0):
        """Rolls initial player stats"""
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
            await self.roll_stats(ctx, times_called)


def setup(bot):
    bot.add_cog(Dice(bot))


def _roll_single_stat():
    # Rolling 4 six sided dice, and dropping the lowest result
    dice = [
        random.choice(range(1, 7))
        for _ in range(4)
    ]
    dice.remove(min(dice))
    stat_value = sum(dice)
    return stat_value

