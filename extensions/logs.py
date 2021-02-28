import datetime
from typing import Optional
import discord
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_message_channel = bot.get_channel(812408474511474709)
        self.log_join_leave_channel = bot.get_channel(812408531772375060)

    @staticmethod
    def make_message_embed(
        meta: dict,
        author: str,
        channel: str,
        _id: tuple,
        message: str,
        attachment: Optional[str]=None
    ) -> discord.Embed:
        """Make embed template used by different events"""

        embed = discord.Embed(
            title=meta.get('title'),
            color=meta.get('color'),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name='Author', value=author, inline=True)
        embed.add_field(name='Channel', value=channel, inline=True)
        embed.add_field(name=_id[0], value=_id[1], inline=True)

        if attachment:
            embed.set_image(url=attachment)

        # chunk message if longer than 1024
        for i, chunk in  enumerate(range(0, len(message), 1024)):
            embed.add_field(
                name=f'{meta.get("m_name")} Part {i+1}',
                value=message[chunk:chunk+1024],
                inline=False
            )

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
            excess = (len(total) - 6000) + 23 # 23 len of Message Error field

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

    @staticmethod
    def make_message(cached_message) -> tuple:
        """Make message from cached_message for embed"""

        message = ''
        attachment_url = None

        if cached_message.content:
                message += f'**message:** {cached_message.content}\n'

        if cached_message.embeds:
            for embed in cached_message.embeds:
                message += f'**embed:** {str(embed.to_dict())}\n'
            message += '\n'

        if cached_message.attachments:
            message += f'**attachment:**'
            attachment_url = cached_message.attachments[0].proxy_url
            message += '\n'

        if cached_message.stickers:
            # no way to test stickers without nitro member
            print(cached_message.stickers)

        return (message, attachment_url)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        """Log deleted messages to log channel"""

        meta = {
            'title': 'Deleted Message',
            'color': discord.Color.from_rgb(255, 0, 0),
            'm_name': 'Message'
        }

        if payload.cached_message:
            message, attachment_url = self.make_message(payload.cached_message)            

            embed = self.make_message_embed(
                meta=meta,
                author=payload.cached_message.author.mention,
                channel=payload.cached_message.channel.mention,
                _id=('Message ID', payload.message_id),
                message=message,
                attachment=attachment_url
            )
        else:
            embed = self.make_message_embed(
                meta=meta,
                author='Unknown',
                channel=self.bot.get_channel(payload.channel_id).mention,
                _id=('Message ID', payload.message_id),
                message='`Message not in cache`'
            )

        # check if embed is too big to send
        self.check_embed_size(embed)

        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        """Log edited messages to log channel"""

        # ignore embeds
        if payload.data['embeds']:
            return

        meta = {
            'title': 'Edited Message',
            'color': discord.Color.from_rgb(255, 250, 0),
            'm_name': 'Old Message'
        }

        if payload.cached_message:
            message, attachment_url = self.make_message(payload.cached_message) 

            embed = self.make_message_embed(
                meta=meta,
                author=payload.cached_message.author.mention,
                channel=payload.cached_message.channel.mention,
                _id=('Message Link', f'[{payload.message_id}]({payload.cached_message.jump_url})'),
                message=message,
                attachment=attachment_url
            )
        else:
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            embed = self.make_message_embed(
                meta=meta,
                author=message.author.mention,
                channel=self.bot.get_channel(payload.channel_id).mention,
                _id=('Message Link', f'[{payload.message_id}]({message.jump_url})'),
                message='`Message not in cache`'
            )

        # check if embed is too big to send
        self.check_embed_size(embed)

        await self.log_channel.send(embed=embed)

    @staticmethod
    def make_member_embed(meta: dict, member: discord.Member) -> discord.Embed:
        """Make embed for member join or leave"""

        # format member account creation time
        creation = (member.created_at - datetime.timedelta(hours=5)).strftime('%B %d, %Y - %-I:%-M%p')

        embed = discord.Embed(
            title=meta.get('title'),
            color=meta.get('color'),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Member', value=member.mention, inline=True)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Account Created', value=creation, inline=False)

        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Log when member joins the guild"""

        meta = {
            'title': 'Member Join',
            'color': discord.Color.from_rgb(0, 255, 30)
        }

        embed = self.make_member_embed(meta, member)

        await self.log_join_leave_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Log when member leaves the guild"""

        meta = {
            'title': 'Member Remove',
            'color': discord.Color.from_rgb(255, 0, 0)
        }

        embed = self.make_member_embed(meta, member)

        await self.log_join_leave_channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logs(bot))
