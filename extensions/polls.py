import asyncio
import discord
from discord.ext import commands
from cfg import cfg
from extensions.moderation import Moderation


class Polls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.green = discord.Color.from_rgb(0, 255, 30)

    @commands.command()
    @commands.has_role(cfg['administration_spacer'].id)
    async def poll(self, ctx: commands.Context, t: int):
        """Create poll for x amount of minutes and then reply to message with
        result
        """

        meta = {
            'title': 'Poll Initiated',
            'color': self.green
        }

        # add reactions
        await ctx.message.add_reaction(cfg['emojis']['yes']['full'])
        await ctx.message.add_reaction(cfg['emojis']['no']['full'])

        await cfg['moderation_channel'].send(
            embed=await Moderation.make_moderation_embed(
                meta=meta,
                admin=ctx.author,
                command=ctx.message.clean_content
            )
        )

        # sleep for x amount of time in seconds
        await asyncio.sleep(t)

        # get results of poll
        yes = 0
        no = 0
        for reaction in ctx.message.reactions:
            if reaction.emoji.id == cfg['emojis']['yes']['id']:
                yes += reaction.count
            elif reaction.emoji.id == cfg['emojis']['no']['id']:
                no += reaction.count

        # reply to message with results of poll
        if yes > no: result = 'Yes'
        elif no > yes: result = 'No'
        else: result = 'Tie'

        await ctx.message.reply(
            f'The result to this poll is: **{result}**\n'
            f'Time: *{t} seconds*\nYes Votes: *{yes}*\nNo Votes: *{no}*'
        )

    @poll.error
    async def poll_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with poll"""

        if isinstance(error, commands.MissingRole):
            return

        await ctx.send(f'Error executing poll:\n`{error}`', delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Polls(bot))
