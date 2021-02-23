import datetime
import discord
from discord.ext import commands
from discord.utils import get


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = bot.get_channel(812408474511474709)
    
    def make_embed(self):
        """Make embed template used by different events"""

        embed = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embed.add_field(name="Field1", value="hi", inline=False)
        embed.add_field(name="Field2", value="hi2", inline=False)

        return embed

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        """Log deleted messages to log channel"""

        time = datetime.datetime.utcnow() - datetime.timedelta(hours=5)

        if payload.cached_message:
            author = payload.cached_message.author
            channel = payload.cached_message.channel

            embed = discord.Embed(
                title='Deleted Message',
                description=str(time),
                color=discord.Color.red()
            )
            embed.add_field(name='Author', value=author.mention, inline=True)
            embed.add_field(name='Channel', value=channel.mention, inline=True)
            embed.add_field(name='Message ID', value=payload.message_id, inline=True)
            embed.add_field(name='Message', value=payload.cached_message.content, inline=False)

        await self.log_channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logs(bot))
