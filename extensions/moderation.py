from typing import Optional
from discord.ext import commands


class Moderation(commands.Cog):
    owner_role_id = 803002510922874980

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = bot.get_guild(803002510864023593)

        self.blacklist_categories = [
            # 805217167847063573, # Register
            # 804825493856976906, # Information
            # 804829689033785344, # Game Logs
            # 812408184719147009  # Discord Logs
        ]

    @commands.command()
    @commands.has_role(owner_role_id)
    async def purge(self, ctx: commands.Context, n: Optional[int]=1):
        """Purge chat messages"""

        if ctx.channel.category_id not in self.blacklist_categories:
            await ctx.channel.purge(limit = n+1)

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with purge"""

        if isinstance(error, commands.MissingPermissions):
            return

        await ctx.send(f'Error executing purge:\n`{error}`')


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
