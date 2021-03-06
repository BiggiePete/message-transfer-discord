import datetime
from typing import Optional
import discord
from discord.ext import commands
from cfg import cfg


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.red = discord.Color.from_rgb(255, 0, 0)
        self.orange = discord.Color.from_rgb(255, 150, 0)
        self.black = discord.Color.from_rgb(0, 0, 0)

        self.purge_blacklist_categories = [
            # 805217167847063573, # Register
            # 804825493856976906, # Information
            # 804829689033785344, # Game Logs
            # 812408184719147009  # Discord Logs
        ]

    @commands.command()
    @commands.has_role(cfg['owner_role'].id)
    async def purge(self, ctx: commands.Context, n: Optional[int]=1):
        """Purge chat messages"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.red
        }

        if ctx.channel.category_id not in self.purge_blacklist_categories:
            await ctx.channel.purge(limit = n+1)
            await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
                meta=meta,
                admin=ctx.author,
                command='purge'
            ))

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with purge"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing purge:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def notyping(self, ctx: commands.Context, member: discord.Member):
        """Gives member No Typing role to prevent member from sending text
        messages
        """

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.black
        }

        await member.add_roles(cfg['no_typing_role'], cfg['trouble_spacer'])
        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command='notyping',
            target=member
        ))

    @notyping.error
    async def notyping_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with notyping"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing notyping:\n`{error}`', delete_after=10)
    
    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def ban(self, ctx: commands.Context, member: discord.Member):
        """Add Ban role to member"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.black
        }

        # remove all roles from member
        await member.edit(roles=[], reason='Banned')

        await member.add_roles(cfg['banned_role'], cfg['trouble_spacer'])
        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command='ban',
            target=member
        ))

    @ban.error
    async def ban_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with ban"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing ban:\n`{error}`', delete_after=10)

    @staticmethod
    async def make_moderation_embed(
        meta: dict,
        admin: discord.Member,
        command: str,
        target: Optional[discord.Member]=None,
    ) -> discord.Embed:
        """Return embed for logging moderation commands"""

        embed = discord.Embed(
            title=meta.get('title'),
            color=meta.get('color'),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=admin.avatar_url)
        embed.add_field(name='Admin', value=admin.mention, inline=True)
        embed.add_field(name='ID', value=admin.id, inline=True)
        embed.add_field(name='Command', value=command, inline=False)

        if target:
            embed.add_field(name='Target', value=target.mention, inline=True)
            embed.add_field(name='ID', value=target.id, inline=True)

        return embed


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
