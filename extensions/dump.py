import csv
from discord.ext import commands

class Dump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.delimiter = '\t'

    @commands.command()
    async def dump_to(self, ctx: commands.Context, filename: str):
        """Dump message history to csv file"""

        with open(f'{filename}.csv', 'w') as f:
            f.write(f'content{self.delimiter}created_at{self.delimiter}pinned\n')
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                if message.author == self.bot.user: continue
                f.write(f'{message.content}{self.delimiter}{message.created_at}{self.delimiter}{message.pinned}\n')

        await ctx.reply('done')

    @dump_to.error
    async def dump_to_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with dump_to"""

        await ctx.send(f'Error executing dump_to:\n`{error}`', delete_after=10)

    @commands.command()
    async def dump_from(self, ctx: commands.Context, filename: str):
        """Dump csv file to discord channel"""

        with open(f'{filename}.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            next(reader) # skip header
            for row in reader:
                message, _, pinned = row
                m = await ctx.send(message)
                # if pinned: await m.pin()

        await ctx.reply('done')

    @dump_from.error
    async def dump_from_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with dump_from"""

        await ctx.send(f'Error executing dump_from:\n`{error}`', delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Dump(bot))
