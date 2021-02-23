import datetime
import discord
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel = bot.get_channel(812408474511474709)
    
    @staticmethod
    def make_embed(title: str, author: str, channel: str, _id: tuple, message: str):
        """Make embed template used by different events"""

        time = datetime.datetime.utcnow() - datetime.timedelta(hours=5)

        embed = discord.Embed(
            title=title,
            description=str(time),
            color=discord.Color.dark_red()
        )
        embed.add_field(name='Author', value=author, inline=True)
        embed.add_field(name='Channel', value=channel, inline=True)
        embed.add_field(name=_id[0], value=_id[1], inline=True)
        embed.add_field(name='Message', value=message[:1024], inline=False)

        return embed

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        """Log deleted messages to log channel"""


        if payload.cached_message:
            message = ''

            if payload.cached_message.content:
                message += f'message: {payload.cached_message.content}\n\n'

            if payload.cached_message.embeds:
                for embed in payload.cached_message.embeds:
                    message += f'embed: {str(embed.to_dict())}\n'
                message += '\n'

            if payload.cached_message.attachments:
                pass

            if payload.cached_message.stickers:
                pass

            embed = self.make_embed(
                title='Deleted Message',
                author=payload.cached_message.author.mention,
                channel=payload.cached_message.channel.mention,
                _id=('Message ID', payload.message_id),
                message=message
            )
        else:
            embed = self.make_embed(
                title='Deleted Message',
                author='Unknown',
                channel=self.bot.get_channel(payload.channel_id).mention,
                _id=('Message ID', payload.message_id),
                message='`Message not in cache`'
            )

        await self.log_channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logs(bot))
