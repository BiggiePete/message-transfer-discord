import discord
from discord.ext import commands, tasks
from discord.utils import get


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = bot.get_guild(803002510864023593)
        self.rules_message_id = 812427095048192000
        self.whitelisted_role = get(self.guild.roles, id=804942365718478928)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Add whitelist role after accepting rules"""

        if payload.message_id == self.rules_message_id:
            if str(payload.emoji) == '✅':
                try:
                    await payload.member.add_roles(self.whitelisted_role)
                except Exception as e:
                    print(f'Error adding whitelist role to member: {e}')


def setup(bot: commands.Bot):
    bot.add_cog(Register(bot))
