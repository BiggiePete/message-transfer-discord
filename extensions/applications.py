import datetime
from discord.ext import commands


class Applications(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.new_applications_channel = bot.get_channel(816416264766881832)
        self.valid_types = {
            'moderator': {
                'review_channel': bot.get_channel(816410656257212416)
            },
            'police': {
                'review_channel': bot.get_channel(816410712645566484)
            }
        }

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


def setup(bot: commands.Bot):
    bot.add_cog(Applications(bot))
