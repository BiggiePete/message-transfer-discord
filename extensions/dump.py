import aiohttp
import asyncio
import io
import json
import discord
from discord.ext import commands


class Dump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def dump_to(self, ctx: commands.Context, filename: str):
        """Dump message history to csv file"""

        data = []
        with open(f'{filename}.json', 'w') as f:
            async for message in ctx.channel.history(limit=None, oldest_first=True):
                if message.author == self.bot.user: continue
                data.append({
                    'content': message.content,
                    'attachments': [x.url for x in message.attachments],
                    'pinned': message.pinned
                })
            data.pop()
            f.write(json.dumps(data))

        await ctx.reply('done')

    @dump_to.error
    async def dump_to_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with dump_to"""

        await ctx.send(f'Error executing dump_to:\n`{error}`', delete_after=10)

    @commands.command()
    async def dump_from(self, ctx: commands.Context, filename: str):
        """Dump csv file to discord channel"""

        with open(f'{filename}.json') as f: data = json.loads(f.read())
        for item in data:
            if not len(item['content']) and not item['attachments']: continue

            attachments = await self.get_attachment_data(item['attachments'])
            print(attachments, len(attachments))

            m = await ctx.send(
                content=item['content'],
                files=[discord.File(a, filename=f'{i}.{item["attachments"][i].split(".")[-1]}') for i, a in enumerate(attachments)]
            )
            if item['pinned']: await m.pin()

        await ctx.reply('done')

    @dump_from.error
    async def dump_from_error(self, ctx: commands.Context, error: commands.CommandError):
        """Function executed when there was an error associated with dump_from"""

        await ctx.send(f'Error executing dump_from:\n`{error}`', delete_after=10)

    async def get_attachment_data(self, urls: list):
        """Create byte objects for uploading attachments"""

        if not urls: return []

        async with aiohttp.ClientSession() as session:
            coroutines = [self.request(session, url) for url in urls]
            attachments = await asyncio.gather(*coroutines)

            return attachments

    @staticmethod
    async def request(session: aiohttp.ClientSession, url: str):
        """Preform asynchronous http request"""

        try:
            async with session.get(url, timeout=2) as response:
                return io.BytesIO(await response.read())
        except Exception as e:
            print('Error with request:', e)


def setup(bot: commands.Bot):
    bot.add_cog(Dump(bot))
