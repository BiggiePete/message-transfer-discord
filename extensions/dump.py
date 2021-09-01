from discord.ext import commands
from cfg import cfg

class Dump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def dump(self, ctx: commands.Context, filename: str):
        """Dump message history to csv file"""

        await ctx.reply('test')

    @dump.error
    async def dump_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with dump"""

        await ctx.send(f'Error executing dump:\n`{error}`', delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Dump(bot))
