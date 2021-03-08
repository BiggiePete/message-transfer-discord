import datetime
from typing import Optional
import discord
from discord.ext import commands
from cfg import cfg, db


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.red = discord.Color.from_rgb(255, 0, 0)
        self.orange = discord.Color.from_rgb(255, 150, 0)
        self.black = discord.Color.from_rgb(0, 0, 0)
        self.green = discord.Color.from_rgb(0, 255, 30)

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
                command=ctx.message.clean_content
            ))

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with purge"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing purge:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def notype(self, ctx: commands.Context, member: discord.Member):
        """Gives member No Type role to prevent member from sending text
        messages
        """

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.orange
        }

        await member.add_roles(cfg['no_type_role'], cfg['trouble_spacer'])
        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command=ctx.message.clean_content,
            target=member
        ))
        await ctx.message.add_reaction(cfg['emojis']['pepeok']['full'])

    @notype.error
    async def notype_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with notype"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing notype:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def oktype(self, ctx: commands.Context, member: discord.Member):
        """Removes member No Type role to allow member to send text  messages"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.green
        }

        await member.remove_roles(cfg['no_type_role'], cfg['trouble_spacer'])
        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command=ctx.message.clean_content,
            target=member
        ))
        await ctx.message.add_reaction(cfg['emojis']['pepeok']['full'])

    @oktype.error
    async def oktype_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with oktype"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing oktype:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def ban(self, ctx: commands.Context, member: discord.Member):
        """Add Ban role to member"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.black
        }

        # remove all roles from member and apply ban roles
        await member.edit(roles=[], reason='Banned')
        await member.add_roles(cfg['banned_role'], cfg['trouble_spacer'])

        # alert user in DM
        await member.send(
            f'**ParadiseRP Ban**\nHi, {member.mention}.\n'
            f'You have been banned. If you wish, you may make a ban application '
            f'in the *new-applications* channel.'
        )

        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command=ctx.message.clean_content,
            target=member
        ))
        await ctx.message.add_reaction(cfg['emojis']['pepeok']['full'])

    @ban.error
    async def ban_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with ban"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing ban:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['owner_role'].id)
    async def resetpoints(self, ctx: commands.Context, member: discord.Member):
        """Reset points of user"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.red
        }

        db.reset_points(member)

        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command=ctx.message.clean_content,
            target=member
        ))
        await ctx.message.add_reaction(cfg['emojis']['pepeok']['full'])

    @resetpoints.error
    async def resetpoints_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with resetpoints"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing resetpoints:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def warn(self, ctx: commands.Context, member: discord.Member, *message: str):
        """Send warn to member"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.orange
        }

        warn_level = db.add_warn(member)

        # send message to target
        message = ' '.join(message) if message else 'N/A'
        await member.send(
            f'**ParadiseRP Warning**\nHi, {member.mention}.\n'
            f'You have been issued a warning by an administrator for the '
            f'following reason:\n{message}'
        )

        # check if warning level has passed 10, if so, apply .ban command
        if warn_level >= 10:
            await self.ban(ctx, member)

        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command=ctx.message.clean_content,
            target=member
        ))
        await ctx.message.add_reaction(cfg['emojis']['pepeok']['full'])

    @warn.error
    async def warn_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with warn"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing warn:\n`{error}`', delete_after=10)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def resetwarn(self, ctx: commands.Context, member: discord.Member):
        """Reset warning level of member"""

        meta = {
            'title': 'Moderation Command Executed',
            'color': self.green
        }

        db.reset_warn(member)

        await cfg['moderation_channel'].send(embed=await self.make_moderation_embed(
            meta=meta,
            admin=ctx.author,
            command=ctx.message.clean_content,
            target=member
        ))
        await ctx.message.add_reaction(cfg['emojis']['pepeok']['full'])

    @resetwarn.error
    async def resetwarn_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with resetwarn"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing resetwarn:\n`{error}`', delete_after=10)

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
