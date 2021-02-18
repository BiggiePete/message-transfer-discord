import json
from discord.ext import commands, tasks
import requests


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_server_status.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('ping'):
            await message.channel.send('pong!')

    # @commands.command()
    # async def hello(self, ctx, *, member: discord.Member = None):
    #     """Says hello"""
    #     member = member or ctx.author
    #     if self._last_member is None or self._last_member.id != member.id:
    #         await ctx.send('Hello {0.name}~'.format(member))
    #     else:
    #         await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
    #     self._last_member = member

    @tasks.loop(seconds=5.0)
    async def get_server_status(self):
        try:
            r = requests.get('http://68.59.13.90:30120/players.json', timeout=3)
            if r:
                print(r.json(), type(r.json()))
        except requests.exceptions.ConnectTimeout:
            print('Request timedout')
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Loops(bot))
