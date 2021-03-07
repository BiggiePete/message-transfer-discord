import datetime
import discord
from discord.ext import commands
from cfg import db, cfg

class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.green = discord.Color.from_rgb(0, 255, 30)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Add points to user for sending message in chat"""

        # check if member exists in db
        if not db.member_exists(message.author):
            db.new_member(message.author)

        db.add_points(message.author, 1)

    @commands.command()
    async def points(self, ctx: commands.Context):
        """Report member's total points"""

        if ctx.channel.category not in cfg['valid_points_categories_ids']:
            return

        points = db.get_member(ctx.author)['points']
        await ctx.send(f'{ctx.author.mention}, you have a total of {points} points.')

    @points.error
    async def points_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with points"""

        await ctx.send(f'Error executing points:\n`{error}`', delete_after=10)

    @commands.command()
    async def toppoints(self, ctx: commands.Context):
        """Embed the top 10 members sorted by points"""

        if ctx.channel.category not in cfg['valid_points_categories_ids']:
            return

        top_members = db.get_top_points()
        top_member = self.bot.get_user(top_members[0][0])

        embed = discord.Embed(
            title='Top Members',
            color=self.green,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=top_member.avatar_url)

        for i, member in enumerate(top_members):
            m = self.bot.get_user(member[0])
            embed.add_field(
                name=f'Position {i+1}',
                value=f'**[{member[1]}]** {m.mention}',
                inline=False
            )

        await ctx.send(embed=embed)

    @toppoints.error
    async def toppoints_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with toppoints"""

        await ctx.send(f'Error executing toppoints:\n`{error}`', delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Points(bot))
