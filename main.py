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
        '**Commands:**\n'
        '   **Anyone:**\n'
        '      **help** - Display this message.\n'
        '      **lookup** *member* - Lookup member attributes.\n'
        '      **points** - See how many points you currently have.\n'
        '      **toppoints** - See the top 10 member\'s with the most points.\n'
        '      **ticket** *message* - Create a new ticket.\n'
        '      **app** *type* *template* - Make a new application.\n'
        '        types: moderator, police, unban.\n\n'
        '   **Trial Moderator+:**\n'
        '      **poll** *time(min)* *content* - Create a new poll that expires after x amount of minutes.\n'
        '      **purge** *n messages* - Bulk delete n amount of message in channel.\n'
        '      **notype** *member* - Disable target member\'s chat privileges.\n'
        '      **oktype** *member* - Enable target member\'s chat privileges.\n'
        '      **warn** *member* - Give target member warning; auto-ban after 10 warns.\n'
        '      **resetwarn** *member* - Reset target\'s warn level.\n'
        '      **ban** *member* - Revoke all roles from target member and they must submit an unban app.\n\n'
        '   **Owner:**\n'
        '      **resetpoints** *member* - Reset target member\'s points.\n'
        '      **loadext** *extension* - Load an extension.\n'
        '      **unloadext** *extension* - Unload an extension.\n'
        '      **reloadext** *extension* - Reload an extension.\n'
        '      **wlmsg** - Make message for reacting to get whitelisted.\n'
        '      **getupdatesmsg** - Make message for reacting to get Server Updates role.\n'
    )


if __name__ == '__main__':
    bot.run('ODE3NzkxMzk1Nzg3NDQwMTU4.YEOplg.azVekNHpODwrVmZmSMatlldo6ds')
