import datetime
import discord
from discord.ext import commands
from discord.utils import get
from cfg import cfg


class Applications(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.valid_reaction_channel_ids = []
        for key in cfg['valid_app_types'].keys():
            self.valid_reaction_channel_ids.append(
                cfg['valid_app_types'][key]['review_channel']
            )

    @commands.command()
    async def app(self, ctx: commands.Context, app_type: str):
        """Make new application"""

        if ctx.channel != cfg['new_applications_channel']:
            await ctx.send(
                f'Sorry {ctx.author.mention}, new applications can only be made '
                f'in the {cfg["new_applications_channel"].mention} channel.',
                delete_after=10
            )
            return
        elif app_type not in list(cfg['valid_app_types'].keys()):
            await ctx.send(
                f'Sorry {ctx.author.mention}, {app_type} is an invalid application type. '
                f'The types available are: {", ".join(cfg["valid_app_types"])}.',
                delete_after=10
            )
            await ctx.message.delete()
            return

        created_at = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        app_review_text = (
            f'**User:** {ctx.author.mention}\n'
            f'**Submitted at:** {created_at.strftime("%B %d, %Y - %-I:%M%p")}\n'
            f'**Application:** {ctx.message.content[4:]}'
        )

        await ctx.message.delete()
        channel = cfg['valid_app_types'][app_type]['review_channel']

        review = await channel.send(app_review_text)
        await review.add_reaction(cfg['emojis']['checkmark'])
        await review.add_reaction(cfg['emojis']['x'])

    @app.error
    async def app_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with reloadext"""

        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.author.mention}, you must supply an application type. '
                f'The types available are: {", ".join(cfg["valid_app_types"])}.\n'
                'Type **.help** if you need more information.',
                delete_after=10
            )
            return

        await ctx.send(f'Error executing app:\n`{error}`', delete_after=10)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Application decision"""

        # check if reaction added is the correct channel
        channel = self.bot.get_channel(payload.channel_id)
        if channel not in self.valid_reaction_channel_ids:
            return

        message = await channel.fetch_message(payload.message_id)
        app_type = channel.name.split('-')[0]
        applicant_id = int(message.content.split('\n')[0].split('@')[-1][:-1])

        # check if reaction added was from proper reviewer
        if cfg['valid_app_types'][app_type]['reviewer_role'] in payload.member.roles:
            applicant = get(self.bot.get_all_members(), id=applicant_id)
            if str(payload.emoji) == cfg['emojis']['checkmark']: # app approved
                try:
                    # for unban app, we actually remove banned role
                    if app_type == 'unban':
                        await applicant.remove_roles(cfg['valid_app_types'][app_type]['role'])
                    else:
                        await applicant.add_roles(cfg['valid_app_types'][app_type]['role'])
                    await self.cleanup_app(message, applicant, True)
                except Exception as e:
                    print(f'Error adding applicant role to member: {e}')
            elif str(payload.emoji) == cfg['emojis']['x']: # app denied
                await self.cleanup_app(message, applicant, False)

    @staticmethod
    async def cleanup_app(
        message: discord.Message,
        applicant: discord.Member,
        decision: bool
    ):
        """Cleanup application after reviewer has made a decision"""

        message_data = message.content.split('\n')
        submission_time = ' '.join(message_data[1].split(' ')[2:])
        app_type = message_data[2].split(':')[1].split(' ')[2]

        if decision: decision = 'APPROVED'
        else: decision = 'DENIED'
        await applicant.send(
            f'**ParadiseRP Application Decision**\nHi, {applicant.mention}.\n'
            f'Your *{app_type}* application submitted on *{submission_time}* '
            f'has been processed.\nYour application decision is: **{decision}**'
        )
        await message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Applications(bot))
