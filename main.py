import os
from cfg import bot, setup_cfg


@bot.event
async def on_ready():
    """When bot is first started"""

    # setup cfg
    setup_cfg()

    # add all extensions
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'extensions')):
        if filename.endswith('.py'):
            bot.load_extension(f'extensions.{filename[:-3]}')

    print(f'Logged in as {bot.user}')


if __name__ == '__main__':
    bot.run('ODgyNjI5ODU4OTg1OTE0NDQ5.YS-LHA.LB6NhWY39TGVn6ZTl9f80O6sxTU')
