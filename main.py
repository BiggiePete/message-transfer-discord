import discord
from discord.ext import commands

# bot = commands.Bot(command_prefix=f'<@!{811718334583930970}>')
bot = commands.Bot(command_prefix=f'.')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send('pong!')


@bot.command()
async def test(ctx, arg):
    print('HERE')
    await ctx.send(arg)


bot.run('ODExNzE4MzM0NTgzOTMwOTcw.YC2Rmw.BLQuxqSiZ20mXLYdkf7r_hC9L_A')
