import aiohttp
import asyncio
import json
import discord
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
        self.get_status.start()
        self.admin_roster.start()

    @commands.command()
    @commands.has_role(cfg['owner_role'].id)
    async def statusupdatemsg(self, ctx: commands.Context):
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

        if payload.message_id == cfg['status_updates_role_message_id']:
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

        if payload.message_id == cfg['status_updates_role_message_id']:
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

        print('scan')

        async with aiohttp.ClientSession() as session:
            coroutines = [self.request(session, url) for url in cfg['status_urls']]
            players, info = await asyncio.gather(*coroutines)

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
        except asyncio.TimeoutError: # server offline
            pass
        except Exception as e:
            print('Error with request:', e)


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
