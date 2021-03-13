import aiohttp
import asyncio
import json
import discord
from discord.ext import commands, tasks
from discord.utils import get
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
        self.get_status.start()
        self.admin_roster.start()

    @commands.command()
    @commands.has_role(cfg['owner_role'].id)
    async def getupdatesmsg(self, ctx: commands.Context):
        """Make message for users to recieve role for server status updates"""

        await ctx.message.delete()
        msg = await ctx.channel.send(
            f'React with {cfg["emojis"]["yes"]["full"]} to be given the '
            f'{cfg["status_updates_role"].mention} role, and receive updates '
            'when the status of the game server changes.'
        )
        await msg.add_reaction(cfg['emojis']['yes']['full'])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Add status updates role to those who enroll"""

        if payload.message_id == cfg['get_updates_role_message_id']:
            if payload.emoji.id == cfg['emojis']['yes']['id']:
                try:
                    await payload.member.add_roles(
                        cfg['status_updates_role'],
                        cfg['other_role_spacer']
                    )
                except Exception as e:
                    print(f'Error adding whitelist role to member: {e}')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Remove whitelist if member unchecks accepting rules"""

        member = await cfg['guild'].fetch_member(payload.user_id)

        if payload.message_id == cfg['get_updates_role_message_id']:
            if payload.emoji.id == cfg['emojis']['yes']['id']:
                try:
                    await member.remove_roles(
                        cfg['status_updates_role'],
                        cfg['other_role_spacer']
                    )
                except Exception as e:
                    print(f'Error adding whitelist role to member: {e}')

    @tasks.loop(minutes=5)
    async def get_status(self):
        """Update status channel names"""

        async with aiohttp.ClientSession() as session:
            coroutines = [self.request(session, url) for url in cfg['status_urls']]
            players, info = await asyncio.gather(*coroutines)

            # update player list
            if players:
                await cfg['player_list_channel'].purge()
                player_list = await self.make_player_list(players)
                msg = await cfg['player_list_channel'].send(
                    cfg['emojis']['kekw']['full'],
                    delete_after=5*60
                )

                await msg.edit(content=player_list)

            if players is None or info is None:
                status = 0
                player_count = 0
                queue_count = 0
            else:
                status = 1
                player_count = len(players)
                queue_count = info['vars']['Queue']

            # check server state changed
            if self.status != status:
                # update channel name
                await cfg['online_channel'].edit(
                    name=f"rp.smileyrp.com: {'Online' if status else 'Offline'}"
                )

                # send update to status update role
                await cfg['announcement_channel'].send(
                    f'{cfg["status_updates_role"].mention}, the status of the server has '
                    f'change from **{"Online" if self.status else "Offline"}** '
                    f'to **{"Online" if status else "Offline"}**. Next scan '
                    'will be in *5 minutes*.'
                )

            # check server player/queue count
            if self.player_count != player_count or self.queue_count != queue_count:
                await cfg['player_count_channel'].edit(
                    name=f"Online Players: {player_count}+{queue_count}/64"
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

    @staticmethod
    async def make_player_list(players: list) -> str:
        """Return a formatted string of the game server playerlist info"""

        pl = '**Online Player List:**\n'
        pl += '**GameID** '.ljust(15)
        pl += '**Discord User** '.ljust(50)
        pl += '**SteamID** '.ljust(31)
        pl += '**Name** '.ljust(50)
        pl += '**Ping**\n'

        for player in players:
            game_id = str(player['id'])

            for _id in player['identifiers']:
                if 'discord' in _id:
                    discord_user = get(cfg['guild'].members, id=int(_id.split(':')[-1]))
                if 'steam' in _id: steam_id = _id.split(':')[-1]

            pl += f'{game_id}'.ljust(20)
            pl += f'{discord_user.mention}'.ljust(62) if discord_user else '@kekw'.ljust(62)
            pl += f'{steam_id}'.ljust(18)
            pl += f'{player["name"]}'.ljust(47)
            pl += f'{player["ping"]}\n'

        return pl

    @staticmethod
    async def request(session: aiohttp.ClientSession, url: str):
        """Preform asynchronous http request"""

        try:
            async with session.get(url, timeout=2) as response:
                data = await response.read()
                return json.loads(data.decode())
        except asyncio.TimeoutError: # server offline
            pass
        except Exception as e:
            print('Error with request:', e)

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
                message += f'{m.mention}, '
            message = message[:-2]
            message += '\n\n'

        await cfg['admin_roster_channel'].purge()
        msg = await cfg['admin_roster_channel'].send(cfg['emojis']['kekw']['full'])
        await msg.edit(content=message)


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
