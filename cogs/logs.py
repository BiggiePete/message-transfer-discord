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

        # chunk message if longer than 1024
        for i, chunk in  enumerate(range(0, len(message), 1024)):
            embed.add_field(name=f'Message Part {i+1}', value=message[chunk:chunk+1024], inline=False)

        return embed

    @staticmethod
    def check_embed_size(embed: discord.Embed):
        """Return embed shortened if longer than the limit of 6000"""

        fields = [embed.title, embed.description, embed.footer.text, embed.author.name]
        fields.extend([field.name for field in embed.fields])
        fields.extend([field.value for field in embed.fields])

        total = ""
        for item in fields:
            total += str(item) if str(item) != 'Embed.Empty' else ''


        if len(total) > 6000:
            excess = (len(total) % 6000) + 23 # 23 len of Message Error field

            for i in range(len(embed.fields)-1, -1, -1):
                if excess <= 0: break

                i_field_len = len(embed.fields[i].name) + len(embed.fields[i].value)
                if i_field_len < excess:
                    embed.remove_field(i)
                    excess = excess - i_field_len
                else:
                    embed.set_field_at(
                        index=-1,
                        name=embed.fields[i].name,
                        value=embed.fields[i].value[0:len(embed.fields[i].value)-excess],
                        inline=embed.fields[i].inline
                    )
                    break

            embed.add_field(name=f'Embed Error', value='Embed > 6000', inline=False)

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

        # check if embed is too big to send
        self.check_embed_size(embed)

        await self.log_channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logs(bot))
