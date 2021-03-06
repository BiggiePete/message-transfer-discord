import discord
from discord.ext import commands
from discord.utils import get
from db import DB

# Init DB
db = DB()
db.init()

# Init Bot
bot = commands.Bot(
    command_prefix='.', # f'<@!{811718334583930970}> ',
    activity=discord.Game(f'KEKW'),
    intents=discord.Intents().all()
)
bot.remove_command('help')

cfg = {}
def setup_cfg():
    """Setup cfg dict after bot is ready"""

    guild = bot.get_guild(817517239166566410)

    _ = {
        'guild': guild,

        # Moderation
        'moderation_channel': bot.get_channel(817841287884439583),
        'owner_role': get(guild.roles, id=817518188048023592),
        'administration_spacer': get(guild.roles, id=817518590676434944),
        'banned_role': get(guild.roles, id=817519224368136193),
        'no_type_role': get(guild.roles, id=817519315539853362),
        'trouble_spacer': get(guild.roles, id=817519452409036800),

        # Stats
        'status_urls': [
            'http://68.59.13.90:30120/players.json',
            'http://68.59.13.90:30120/smileyrp_queue/count'
        ],
        'online_channel': bot.get_channel(817524069599674398),
        'player_count_channel': bot.get_channel(817524187676934177),
        'total_users_channel': bot.get_channel(817524228038328331),

        # Registration
        'whitelist_message_id': 817794617742590005,
        'whitelisted_role': get(guild.roles, id=817519095436017734),
        'general_role_spacer': get(guild.roles, id=817519199693176842),

        # Applications
        'new_applications_channel': bot.get_channel(817525072016310313),
        'valid_app_types': {
            'moderator': {
                'review_channel': bot.get_channel(817525113528123403),
                'reviewer_role': get(guild.roles, id=817518857953738843),
                'role': get(guild.roles, id=817518541133185075),
                'role_spacer': get(guild.roles, id=817518590676434944)
            },
            'police': {
                'review_channel': bot.get_channel(817525141579890699),
                'reviewer_role': get(guild.roles, id=817518884591501312),
                'role': get(guild.roles, id=817518969350520873),
                'role_spacer': get(guild.roles, id=817519065098354718)
            },
            'unban': {
                'review_channel': bot.get_channel(817525168275849236),
                'reviewer_role': get(guild.roles, id=817518910332993627),
                'role': get(guild.roles, id=817519224368136193),
                'role_spacer': get(guild.roles, id=817519452409036800)
            }
        },

        # Logs
        'log_message_channel': bot.get_channel(817526349290930246),
        'log_join_leave_channel': bot.get_channel(817526320011018291),
        'log_kick_ban_channel': bot.get_channel(817526296108072970),
        'log_role_update_channel': bot.get_channel(817526376856289320),

        # Emojis
        'emojis': {
            'yes': {
                'id': 817529463440801812,
                'full': '<:yes:817529463440801812>'
            },
            'no': {
                'id': 817529387792597034,
                'full': '<:no:817529387792597034>'
            }
        }
    }

    cfg.update(_)
