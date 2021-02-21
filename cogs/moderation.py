from typing import Optional
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.black_list_clear_channel_ids = [
            805217207305895987
        ]

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, n: Optional[int]=1):
        """Purge chat messages"""

        if ctx.channel.id not in self.black_list_clear_channel_ids:
            await ctx.channel.purge(limit = n+1)

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with purge"""

        if isinstance(error, commands.MissingPermissions):
            return

        await ctx.send(f'Error executing purge:\n`{error}`')


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
