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

    guild = bot.get_guild(817517239166566410)

    # smiley = {
    #     'guild': guild,
    #     'owner_role': get(guild.roles, id=803002510922874980),

    #     # Stats
    #     'status_urls': [
    #         'http://68.59.13.90:30120/players.json',
    #         'http://68.59.13.90:30120/smileyrp_queue/count'
    #     ],
    #     'online_channel': bot.get_channel(804825065060302889),
    #     'player_count_channel': bot.get_channel(804825835344494612),
    #     'total_users_channel': bot.get_channel(804825997161005146),

    #     # Registration
    #     'whitelist_message_id': 812427095048192000,
    #     'whitelisted_role': get(guild.roles, id=804942365718478928),
    #     'general_role_spacer': get(guild.roles, id=816801261247922176),

    #     # Applications
    #     'new_applications_channel': bot.get_channel(816416264766881832),
    #     'valid_app_types': {
    #         'moderator': {
    #             'review_channel': bot.get_channel(816410656257212416),
    #             'reviewer_role': get(guild.roles, id=816458283019272212),
    #             'role': get(guild.roles, id=803002510922874976),
    #             'role_spacer': get(guild.roles, id=816797670139232276)
    #         },
    #         'police': {
    #             'review_channel': bot.get_channel(816410712645566484),
    #             'reviewer_role': get(guild.roles, id=816465523239550976),
    #             'role': get(guild.roles, id=816387375218556959),
    #             'role_spacer': get(guild.roles, id=816806694176161803)
    #         },
    #         'unban': {
    #             'review_channel': bot.get_channel(816763576408342538),
    #             'reviewer_role': get(guild.roles, id=816763356290744361),
    #             'role': get(guild.roles, id=816763651956539414),
    #             'role_spacer': get(guild.roles, id=816801869602619452)
    #         }
    #     },

    #     # Logs
    #     'log_message_channel': bot.get_channel(812408474511474709),
    #     'log_join_leave_channel': bot.get_channel(812408531772375060),
    #     'log_kick_ban_channel': bot.get_channel(812408406530326538),
    #     'log_role_update_channel': bot.get_channel(817508873694478386),

    #     # Emojis
    #     'emojis': {
    #         'yes': {
    #             'id': 817497505847312404,
    #             'full': '<:yes:817497505847312404>'
    #         },
    #         'no': {
    #             'id': 817497411257368627,
    #             'full': '<:no:817497411257368627>'
    #         }
    #     }
    # }

    arp = {
        'guild': guild,
        'owner_role': get(guild.roles, id=817518188048023592),

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

    cfg.update(arp)
