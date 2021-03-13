import os
from discord.ext import commands
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


@bot.command()
async def help(ctx: commands.Context):
    """Help command"""

    await ctx.send('ParadiseRP Help\n'
        'Events:\n'
        '   Message edit and delete logs\n'
        '   Member join or leave(self, kick, ban) logs\n'
        '   Member role add or remove logs\n'
        '   Points awarded for sending messages\n'
        '   Points awarded for being in a voice channel\n'
        '   Accept rules to be whitelisted\n'
        '   React to get server state changes\n'
        '   Get server status every 5 minutes\n'
        '   Get online player list every 5 minutes\n'
        '   Get admin roster every 5 minutes\n'
        'Commands:\n'
        '   **help**  - (anyone) Display this message\n'
        '   **points** - (anyone) See how many points you currently have\n'
        '   **toppoints** - (anyone) See the top 10 member\'s with the most points\n'
        '   **ticket** *message* - (anyone) Create a new ticket\n'
        '   **app** *type* *template* - (everyone) Make a new application\n'
        '     types: moderator, police, unban\n'
        '   **poll** *time(min)* *content* - (trial moderator+) Create a new poll that expires after x amount of minutes\n'
        '   **purge** *n messages* - (trial moderator+) Bulk delete n amount of message in channel\n'
        '   **notype** *member* - (trial moderator+) Disable target member\'s chat privileges\n'
        '   **oktype** *member* - (trial moderator+) Enable target member\'s chat privileges\n'
        '   **warn** *member* - (trial moderator+) Give target member warning; auto-ban after 10 warns\n'
        '   **resetwarn** *member* - (trial moderator+) Reset target\'s warn level\n'
        '   **ban** *member* - (trial moderator+) Revoke all roles from target member and they must submit an unban app\n'
        '   **resetpoints** *member* - (owner) Reset target member\'s points\n'
        '   **loadext** *extension* - (owner) Load an extension\n'
        '   **unloadext** *extension* - (owner) Unload an extension\n'
        '   **reloadext** *extension* - (owner) Reload an extension\n'
        '   **wlmsg** - (owner) Make message for reacting to get whitelisted\n'
        '   **getupdatesmsg** - (owner) Make message for reacting to get Server Updates role\n'
    )


if __name__ == '__main__':
    bot.run('ODE3NzkxMzk1Nzg3NDQwMTU4.YEOplg.azVekNHpODwrVmZmSMatlldo6ds')
