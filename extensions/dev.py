from typing import Optional
from discord.ext import commands


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def loadext(self, ctx: commands.Context, extension: str):
        """Load an extension"""

        if ctx.message.author.id != 841043611414954034: return

        try:
            self.bot.load_extension(f'extensions.{extension}')
        except Exception as e:
            await ctx.send(f'Error loading extension:\n`{e}`', delete_after=10)

    @loadext.error
    async def loadext_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with loadext"""

        if isinstance(error, commands.CheckFailure): return

        await ctx.send(f'Error executing loadext:\n`{error}`', delete_after=10)

    @commands.command()
    async def unloadext(self, ctx: commands.Context, extension: str):
        """Unload an extension"""

        if ctx.message.author.id != 841043611414954034: return

        try:
            self.bot.unload_extension(f'extensions.{extension}')
        except Exception as e:
            await ctx.send(f'Error unloadeding extension:\n`{e}`', delete_after=10)

    @unloadext.error
    async def unloadext_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with unloadext"""

        if isinstance(error, commands.CheckFailure): return

        await ctx.send(f'Error executing unloadext:\n`{error}`', delete_after=10)

    @commands.command()
    async def reloadext(self, ctx: commands.Context, extension: str):
        """Reload an extension"""

        if ctx.message.author.id != 841043611414954034: return

        try:
            self.bot.reload_extension(f'extensions.{extension}')
        except Exception as e:
            await ctx.send(f'Error reloading extension:\n`{e}`', delete_after=10)

    @reloadext.error
    async def reloadext_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with reloadext"""

        if isinstance(error, commands.CheckFailure): return

        await ctx.send(f'Error executing reloadext:\n`{error}`', delete_after=10)
    
    @commands.command()
    async def purge(self, ctx: commands.Context, n: Optional[int]=1):
        """Purge chat messages"""

        if ctx.message.author.id != 841043611414954034: return

        await ctx.channel.purge(limit = n+1)

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with purge"""

        await ctx.send(f'Error executing purge:\n`{error}`', delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Dev(bot))
