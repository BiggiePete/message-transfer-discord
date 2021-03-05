import discord
from discord.ext import commands
from discord.utils import get


bot = commands.Bot(
    command_prefix='.', # f'<@!{811718334583930970}> ',
    activity=discord.Game(f'KEKW'),
    intents=discord.Intents().all()
)
bot.remove_command('help')

cfg = {}
def setup_cfg():
    """Setup cfg dict after bot is ready"""

    guild = bot.get_guild(803002510864023593)

    _ = {
        'guild': guild,
        'owner_role': get(guild.roles, id=803002510922874980),

        # Stats
        'status_urls': [
            'http://68.59.13.90:30120/players.json',
            'http://68.59.13.90:30120/smileyrp_queue/count'
        ],
        'online_channel': bot.get_channel(804825065060302889),
        'player_count_channel': bot.get_channel(804825835344494612),
        'total_users_channel': bot.get_channel(804825997161005146),

        # Registration
        'rules_message_id': 812427095048192000,
        'whitelisted_role': get(guild.roles, id=804942365718478928),
        'general_role_spacer': get(guild.roles, id=816801261247922176),

        # Applications
        'new_applications_channel': bot.get_channel(816416264766881832),
        'valid_app_types': {
            'moderator': {
                'review_channel': bot.get_channel(816410656257212416),
                'reviewer_role': get(guild.roles, id=816458283019272212),
                'role': get(guild.roles, id=803002510922874976),
                'role_spacer': get(guild.roles, id=816797670139232276)
            },
            'police': {
                'review_channel': bot.get_channel(816410712645566484),
                'reviewer_role': get(guild.roles, id=816465523239550976),
                'role': get(guild.roles, id=816387375218556959),
                'role_spacer': get(guild.roles, id=816806694176161803)
            },
            'unban': {
                'review_channel': bot.get_channel(816763576408342538),
                'reviewer_role': get(guild.roles, id=816763356290744361),
                'role': get(guild.roles, id=816763651956539414),
                'role_spacer': get(guild.roles, id=816801869602619452)
            }
        },

        # Logs
        'log_message_channel': bot.get_channel(812408474511474709),
        'log_join_leave_channel': bot.get_channel(812408531772375060),
        'log_kick_ban_channel': bot.get_channel(812408406530326538),

        # Emojis
        'emojis': {
            'checkmark': '✅',
            'x': '❌'
        }
    }

    cfg.update(_)