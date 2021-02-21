from discord.ext import commands


class Dev(commands.Cog):
    owner_role_id = 803002510922874980

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(owner_role_id)
    async def loadext(self, ctx: commands.Context, extension: str):
        """Load an extension"""

        try:
            self.bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'Successfully loaded extension `{extension}`')
        except Exception as e:
            await ctx.send(f'Error loading extension:\n`{e}`')

    @loadext.error
    async def loadext_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with loadext"""

        if isinstance(error, commands.CheckFailure):
            return

        await ctx.send(f'Error executing loadext:\n`{error}`')

    @commands.command()
    @commands.has_role(owner_role_id)
    async def unloadext(self, ctx: commands.Context, extension: str):
        """Unload an extension"""

        try:
            self.bot.unload_extension(f'cogs.{extension}')
            await ctx.send(f'Successfully unloaded extension `{extension}`')
        except Exception as e:
            await ctx.send(f'Error unloadeding extension:\n`{e}`')

    @unloadext.error
    async def unloadext_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with unloadext"""

        if isinstance(error, commands.CheckFailure):
            return

        await ctx.send(f'Error executing unloadext:\n`{error}`')
    
    @commands.command()
    @commands.has_role(owner_role_id)
    async def reloadext(self, ctx: commands.Context, extension: str):
        """Reload an extension"""

        try:
            self.bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'Successfully reloaded extension `{extension}`')
        except Exception as e:
            await ctx.send(f'Error reloading extension:\n`{e}`')

    @reloadext.error
    async def reloadext_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with reloadext"""

        if isinstance(error, commands.CheckFailure):
            return

        await ctx.send(f'Error executing reloadext:\n`{error}`')


def setup(bot: commands.Bot):
    bot.add_cog(Dev(bot))
