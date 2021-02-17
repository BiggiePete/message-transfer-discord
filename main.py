import discord

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send('pong!')


client.run('ODExNzE4MzM0NTgzOTMwOTcw.YC2Rmw.BLQuxqSiZ20mXLYdkf7r_hC9L_A')
