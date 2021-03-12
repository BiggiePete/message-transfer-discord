import aiohttp
import asyncio
import json
from discord.ext import commands, tasks
from cfg import cfg

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # statuses
        self.status = None
        self.player_count = None
        self.queue_count = None
        self.total_users = None

        # start tasks
        # self.get_status.start()
        # self.admin_roster.start()

    @tasks.loop(minutes=1)
    async def get_status(self):
        """Update status channel names"""

        async with aiohttp.ClientSession() as session:
            coroutines = [self.request(session, url) for url in cfg['status_urls']]
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
                await cfg['online_channel'].edit(name =
                    f"rp.smileyrp.com: {'Online' if status else 'Offline'}"
                )

            # check server player/queue count
            if self.player_count != player_count or self.queue_count != queue_count:
                await cfg['player_count_channel'].edit(name =
                    f"Online Players: {player_count}+{queue_count}/64"
                )

            # check change in discord member count
            if self.total_users != cfg['guild'].member_count:
                await cfg['total_users_channel'].edit(
                    name=f'Total Users: {cfg["guild"].member_count}'
                )

            # update state
            self.status = status
            self.player_count = player_count
            self.queue_count = queue_count
            self.total_users = cfg['guild'].member_count

    @tasks.loop(minutes=5)
    async def admin_roster(self):
        """Update admin roster on loop based off discord status"""

        # get all members with administration_spacer role
        admins = cfg['administration_spacer'].members

        # loop through all admins and make dict with key as role and value as members
        roles = {}
        for admin in admins:
            if admin.top_role not in roles:
                roles[admin.top_role] = []
            roles[admin.top_role].append(admin)

        # make formatted message
        message = ''
        for role, members in roles.items():
            message += f'**{role.name}**\n'
            for m in members:
                message += f'{m.name}#{m.discriminator}, '
            message = message[:-2]
            message += '\n\n'

        await cfg['admin_roster_channel'].purge()
        await cfg['admin_roster_channel'].send(message)

    @staticmethod
    async def request(session: aiohttp.ClientSession, url: str):
        """Preform asynchronous http request"""

        try:
            async with session.get(url, timeout=2) as response:
                data = await response.read()
                return json.loads(data.decode())
        except asyncio.TimeoutError:
            print('Server offline')
        except Exception as e:
            print('Error with request:', e)


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
