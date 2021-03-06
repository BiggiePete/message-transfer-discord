import discord
from discord.ext import commands
from cfg import cfg


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(cfg['owner_role'].id)
    async def wlmsg(self, ctx: commands.Context):
        """Make message that users must agree with to be whitelisted"""

        await ctx.message.delete()
        msg = await ctx.channel.send(
            f'After you have read the rules, react to this message with '
            f'{cfg["emojis"]["yes"]["full"]} to be whitelisted.'
        )
        await msg.add_reaction(cfg['emojis']['yes']['full'])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Add whitelist role after accepting rules"""

        if payload.message_id == cfg['whitelist_message_id']:
            if payload.emoji.id == cfg['emojis']['yes']['id']:
                try:
                    await payload.member.add_roles(
                        cfg['whitelisted_role'],
                        cfg['general_role_spacer']
                    )
                except Exception as e:
                    print(f'Error adding whitelist role to member: {e}')


def setup(bot: commands.Bot):
    bot.add_cog(Register(bot))
