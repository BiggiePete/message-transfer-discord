import discord
from discord.ext import commands
from cfg import db

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


def setup(bot: commands.Bot):
    bot.add_cog(Points(bot))
