import datetime
import discord
from discord.ext import commands
from discord.utils import get
from cfg import cfg


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """On message event to check if message is not a command in new-tickets
        channel
        """

        if message.author == self.bot.user: return

        if message.channel == cfg['new_ticket_channel'] \
        and message.content[:8] != '.ticket ':
            await message.delete()

    @commands.command()
    async def ticket(self, ctx: commands.Context, *, message):
        """Make new application"""

        if ctx.channel != cfg['new_ticket_channel']:
            await ctx.send(
                f'Sorry {ctx.author.mention}, new tickets can only be made '
                f'in the {cfg["new_ticket_channel"].mention} channel.',
                delete_after=10
            )
            return

        created_at = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        created_at = created_at.strftime("%B %d, %Y - %-I:%M%p")

        ticket_text = (
            f'**User:** {ctx.author.mention}\n'
            f'**Submitted at:** {created_at}\n'
            f'**Ticket:** {ctx.message.content[8:]}'
        )

        await ctx.message.delete()

        # get proper channel if donator
        if cfg['vip_spacer'] in ctx.author.roles:
            channel = cfg['high_priority_channel']
        else:
            channel = cfg['low_priority_channel']

        # move ticket to review channel
        review = await channel.send(ticket_text)
        await review.add_reaction(cfg['emojis']['yes']['full'])

        # send confirmation message to author saying their application was submitted
        await ctx.author.send(
            f'**ParadiseRP Ticket Submitted**\nHi, {ctx.author.mention}.\n'
            f'Your ticket has successfully been submitted at *{created_at}*. '
            f'A member of the administrative team will begin to review your ticket.'
        )

    @ticket.error
    async def ticket_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with ticket"""

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.author.mention}, you must supply a message with your ticket.',
                delete_after=10
            )
            return

        await ctx.send(f'Error executing app:\n`{error}`', delete_after=10)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Ticket reviewed"""

        # check if reaction added is the correct channel
        channel = self.bot.get_channel(payload.channel_id)
        if channel != cfg['high_priority_channel'] and \
        channel != cfg['low_priority_channel']:
            return

        message = await channel.fetch_message(payload.message_id)
        applicant_id = int(message.content.split('\n')[0].split('@')[-1][:-1])

        # check if reaction added was from proper reviewer
        if cfg['administration_spacer'] in payload.member.roles and \
        payload.member != self.bot.user:
            applicant = get(self.bot.get_all_members(), id=applicant_id)
            if payload.emoji.id == cfg['emojis']['yes']['id']: # close ticket
                await self.cleanup_ticket(message, applicant, payload.member)

    @staticmethod
    async def cleanup_ticket(
        message: discord.Message,
        applicant: discord.Member,
        reviewer: discord.Member
    ):
        """Cleanup ticket after reviewer has closed ticket"""

        message_data = message.content.split('\n')
        submission_time = ' '.join(message_data[1].split(' ')[2:])

        await applicant.send(
            f'**ParadiseRP Ticket Closed**\nHi, {applicant.mention}.\n'
            f'Your ticket submitted on *{submission_time}* has been processed '
            f'and closed.\nThank you.'
        )
        await message.delete()

        # log ticket
        archive = await cfg['log_closed_tickets_channel'].send(
            f'{message.content}\n'
            f'**Reviewer**: {reviewer.mention}'
        )
        await archive.add_reaction(cfg['emojis']['yes']['full'])


def setup(bot: commands.Bot):
    bot.add_cog(Tickets(bot))
