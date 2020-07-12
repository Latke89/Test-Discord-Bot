import requests
import os
import json
from discord.ext import commands
from src.Models.Game_Mechanics.SpellDescription import SpellDescription

BASE_URL = os.getenv('BASE_URL')


class Spells(commands.Cog):
    __endpoint = 'spells/'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spell')
    async def get_spell(self, ctx, *args):
        spell_name: str
        if len(args) > 1:
            spell_name = '-'.join(args)
        else:
            spell_name = args[0]
        url = f'{BASE_URL}{self.__endpoint}{spell_name.lower()}'
        resp = requests.get(url)
        if resp.status_code != 200:
            print(resp)
            print(f'GET {url} {resp.status_code}')
            await ctx.send('Unable to find spell =\'(')
        else:
            nl = '\n'
            print(resp.json())
            spell = SpellDescription(resp.json())
            if not hasattr(spell, "higher_level"):
                await ctx.send(f'{spell.name}\nLevel: {spell.level}\n{spell.school["name"]}\n'
                               f'Range: {spell.range}\nComponents: {", ".join(spell.components)}\n'
                               f'Duration: {spell.duration}\n{nl.join(spell.desc)}\n')
            else:
                await ctx.send(f'{spell.name}\nLevel: {spell.level}\n{spell.school["name"]}\n'
                               f'Range: {spell.range}\nComponents: {", ".join(spell.components)}\n'
                               f'Duration: {spell.duration}\n{nl.join(spell.desc)}\n'
                               f'At Higher Levels: {", ".join(spell.higher_level)}')


def setup(bot):
    bot.add_cog(Spells(bot))
