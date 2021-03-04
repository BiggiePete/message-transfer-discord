import os
from cfg import bot, setup

@bot.event
async def on_ready():
    """When bot is first started"""

    # setup cfg
    setup()

    # add all extensions
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'extensions')):
        if filename.endswith('.py'):
            bot.load_extension(f'extensions.{filename[:-3]}')

    print(f'Logged in as {bot.user}')

if __name__ == '__main__':
    bot.run('ODExNzE4MzM0NTgzOTMwOTcw.YC2Rmw.BLQuxqSiZ20mXLYdkf7r_hC9L_A')
