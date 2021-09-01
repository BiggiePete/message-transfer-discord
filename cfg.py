import discord
from discord.ext import commands

# Init Bot
bot = commands.Bot(
    command_prefix='.',
    activity=discord.Game(f'Transfer'),
    intents=discord.Intents().all()
)
bot.remove_command('help')

cfg = {}
def setup_cfg():
    """Setup cfg dict after bot is ready"""

    guild = bot.get_guild(878790933062246430)

    _ = {
        'guild': guild
    }

    cfg.update(_)
