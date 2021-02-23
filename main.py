import os
import discord
from discord.ext import commands

# bot = commands.Bot(command_prefix=f'<@!{811718334583930970}> ')
bot = commands.Bot(command_prefix='.', activity=discord.Game(f'KEKW'))


@bot.event
async def on_ready():
    """When bot is first started"""

    # add all extensions
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs')):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    print(f'Logged in as {bot.user}')

bot.run('ODExNzE4MzM0NTgzOTMwOTcw.YC2Rmw.BLQuxqSiZ20mXLYdkf7r_hC9L_A')
