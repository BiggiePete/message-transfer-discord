import aiohttp
import asyncio
import json
import discord
from discord.ext import commands, tasks

class Loops(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = bot.get_guild(803002510864023593)

        # channels
        self.online_channel = bot.get_channel(804825065060302889)
        self.player_count_channel = bot.get_channel(804825835344494612)
        self.total_users_channel = bot.get_channel(804825997161005146)

        # statuses
        self.status = None
        self.player_count = None
        self.queue_count = None
        self.total_users = None

        self.status_urls = [
            'http://68.59.13.90:30120/players.json',
            'http://68.59.13.90:30120/smileyrp_queue/count'
        ]

        # start tasks
        self.get_status.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('ping'):
            await message.channel.send('pong!')

    @tasks.loop(minutes=1)
    async def get_status(self):
        """update status channel names"""

        async with aiohttp.ClientSession() as session:
            coroutines = [self.request(session, url) for url in self.status_urls]
            players, queue = await asyncio.gather(*coroutines)

            if players is None or queue is None:
                status = 0
                player_count = 0
                queue_count = 0
            else:
                status = 1
                player_count = len(players)
                queue_count = queue['count']

            # check server dead or alive
            if self.status != status:
                await self.online_channel.edit(name =
                    f"rp.smileyrp.com: {'Online' if status else 'Offline'}"
                )

            # check server player/queue count
            if self.player_count != player_count or self.queue_count != queue_count:
                await self.player_count_channel.edit(name =
                    f"Online Players: {player_count}+{queue_count}/64"
                )

            # check change in discord member count
            if self.total_users != self.guild.member_count:
                await self.total_users_channel.edit(
                    name=f'Total Users: {self.guild.member_count}'
                )

            # update state
            self.status = status
            self.player_count = player_count
            self.queue_count = queue_count
            self.total_users = self.guild.member_count
            

    @staticmethod
    async def request(session: aiohttp.ClientSession, url: str):
        """preform asynchronous http request"""

        try:
            async with session.get(url, timeout=2) as response:
                data = await response.read()
                return json.loads(data.decode())
        except asyncio.TimeoutError as e:
            print('Request timed out:', e)
        except Exception as e:
            print('Error with request:', e)


def setup(bot: commands.Bot):
    bot.add_cog(Loops(bot))
