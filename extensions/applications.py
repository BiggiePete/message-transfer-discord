import datetime
import discord
from discord.ext import commands
from discord.utils import get


class Applications(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = bot.get_guild(803002510864023593)

        self.new_applications_channel = bot.get_channel(816416264766881832)
        self.valid_types = {
            'moderator': {
                'review_channel': bot.get_channel(816410656257212416),
                'reviewer_role': get(self.guild.roles, id=816458283019272212),
                'role': get(self.guild.roles, id=803002510922874976)
            },
            'police': {
                'review_channel': bot.get_channel(816410712645566484),
                'reviewer_role': get(self.guild.roles, id=816465523239550976),
                'role': get(self.guild.roles, id=816387375218556959)
            },
            'unban': {
                'review_channel': bot.get_channel(816763576408342538),
                'reviewer_role': get(self.guild.roles, id=816763356290744361),
                'role': get(self.guild.roles, id=816763651956539414)
            }
        }

        self.valid_reaction_channel_ids = []
        for key in self.valid_types.keys():
            self.valid_reaction_channel_ids.append(self.valid_types[key]['review_channel'])

    @commands.command()
    async def app(self, ctx: commands.Context, type: str):
        """Make new application"""

        if ctx.channel != self.new_applications_channel:
            await ctx.send('wrong channel dumE')
            return
        elif type not in list(self.valid_types.keys()):
            await ctx.send('wrong type dumE')
            return

        created_at = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        app_review_text = (
            f'**User:** {ctx.author.mention}\n'
            f'**Submitted at:** {created_at.strftime("%B %d, %Y - %-I:%M%p")}\n'
            f'**Application:** {ctx.message.content[4:]}'
        )

        await ctx.message.delete()
        channel = self.valid_types[type]['review_channel']

        review = await channel.send(app_review_text)
        await review.add_reaction('✅')
        await review.add_reaction('❌')

    @app.error
    async def app_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with reloadext"""

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'{ctx.author.mention}, you must supply an application type. '
                f'The types available are: {", ".join(self.valid_types)}.\n'
                'Type **.help** if you need more information.'
            )
            return

        await ctx.send(f'Error executing app:\n`{error}`')

    @staticmethod
    async def cleanup_app(
        message: discord.Message,
        applicant: discord.Member,
        decision: bool
    ):
        """Cleanup application after reviewer has made a decision"""

        message_data = message.content.split('\n')
        submission_time = ' '.join(message_data[1].split(' ')[2:])
        type = message_data[2].split(':')[1].split(' ')[2]

        if decision: decision = 'APPROVED'
        else: decision = 'DENIED'
        await applicant.send(
            f'**ParadiseRP Application Decision**\nHi, {applicant.mention}.\n'
            f'Your *{type}* application submitted on *{submission_time}* '
            f'has been processed.\nYour application decision is: **{decision}**'
        )
        await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Application decision"""

        # check if reaction added is the correct channel
        channel = self.bot.get_channel(payload.channel_id)
        if channel not in self.valid_reaction_channel_ids:
            return

        message = await channel.fetch_message(payload.message_id)
        type = channel.name.split('-')[0]
        applicant_id = int(message.content.split('\n')[0].split('@')[-1][:-1])

        # check if reaction added was from proper reviewer
        if self.valid_types[type]['reviewer_role'] in payload.member.roles:
            applicant = get(self.bot.get_all_members(), id=applicant_id)
            if str(payload.emoji) == '✅': # app approved
                try:
                    # for unban app, we actually remove banned role
                    if type == 'unban':
                        await applicant.remove_roles(self.valid_types[type]['role'])
                    else:
                        await applicant.add_roles(self.valid_types[type]['role'])
                    await self.cleanup_app(message, applicant, True)
                except Exception as e:
                    print(f'Error adding applicant role to member: {e}')
            elif str(payload.emoji) == '❌': # app denied
                await self.cleanup_app(message, applicant, False)


def setup(bot: commands.Bot):
    bot.add_cog(Applications(bot))
