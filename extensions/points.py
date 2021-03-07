import discord
from discord.ext import commands
from cfg import db, cfg

class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Add points to user for sending message in chat"""

        # check if member exists in db
        if not db.member_exists(message.author):
            db.new_member(message.author)

        db.add_points(message.author, 1)

    @commands.command()
    async def points(self, ctx: commands.Context):
        """Report members total points"""

        if ctx.channel.category not in cfg['valid_points_categories_ids']:
            return

        points = db.get_member(ctx.author)['points']
        await ctx.send(f'{ctx.author.mention}, you have a total of {points} points.')

    @points.error
    async def points_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with points"""

        await ctx.send(f'Error executing points:\n`{error}`', delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Points(bot))
