import sqlite3
import discord


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('discord.db')
        self.c = self.connection.cursor()

        self.fields = '''
            name, discriminator, discord_id, joined_guild, points,
            lifetime_points, warn_level, lifetime_warns, is_d_banned,
            lifetime_d_bans
        '''

    def init(self):
        """"Make tables for db"""

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                discriminator TEXT NOT NULL,
                discord_id INTEGER,
                joined_guild DATE NOT NULL,
                points REAL NOT NULL,
                lifetime_points REAL NOT NULL,
                warn_level INTEGER NOT NULL,
                lifetime_warns INTEGER NOT NULL,
                is_d_banned INTEGER NOT NULL,
                lifetime_d_bans INTEGER NOT NULL
            );
        ''')
        self.connection.commit()

    def new_member(self, member: discord.Member):
        """Create new entry in members table of member"""

        self.c.execute(f'''
            INSERT INTO members ({self.fields}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (
            member.name,
            member.discriminator,
            member.id,
            member.joined_at,
            0, 0, 0, 0, 0, 0
        ))
        self.connection.commit()

    def member_exists(self, member: discord.Member):
        """Return if member exists in db referenced from discord.Member"""

        self.c.execute('''
            SELECT 1 from members WHERE discord_id=?;
        ''', (member.id,))

        if not self.c.fetchone(): return False
        return True

    def get_member(self, member: discord.Member) -> dict:
        """Return member from db referenced from discord.Member"""

        self.c.execute(f'''
            SELECT {self.fields} FROM members WHERE discord_id=?;
        ''', (member.id,))

        member = self.c.fetchone()
        member = {
            'id': member[0],
            'name': member[0],
            'discriminator': member[1],
            'discord_id': member[2],
            'joined_guild': member[3],
            'points': member[4],
            'lifetime_points': member[5],
            'warn_level': member[6],
            'lifetime_warn': member[7]
        }

        return member

    def add_points(self, member: discord.Member, points: int):
        """Add points to discord member"""

        self.c.execute('''
            UPDATE members SET points=points+?, lifetime_points=lifetime_points+?
            WHERE discord_id=?;
        ''', (points, points, member.id,))
        self.connection.commit()

    def reset_points(self, member: discord.Member):
        """Reset points of discord member"""

        self.c.execute('''
            UPDATE members SET points=0 WHERE discord_id=?;
        ''',  (member.id,))
        self.connection.commit()


    def get_top_points(self) -> list:
        """Return a sorted list of the top 10 members sorted by points"""

        self.c.execute('''
            SELECT discord_id, points FROM members ORDER BY points DESC LIMIT 10;
        ''')

        return self.c.fetchall()

    def add_warn(self, member: discord.Member) -> int:
        """Add warning to member and return new warning level"""

        self.c.execute('''
            UPDATE members SET warn_level=warn_level+1, lifetime_warns=lifetime_warns+1
            WHERE discord_id=?;
        ''', (member.id,))
        self.connection.commit()

        return self.get_member(member)['warn_level']

    def reset_warn(self, member: discord.Member):
        """Reset warning level of member"""

        self.c.execute('''
            UPDATE members SET warn_level=0 WHERE discord_id=?;
        ''', (member.id,))
        self.connection.commit()

    def is_d_banned(self, member: discord.Member) -> bool:
        """Check if member is d_banned"""

        self.c.execute('''
            SELECT is_d_banned from members WHERE discord_id=?;
        ''', (member.id,))

        if self.c.fetchone()[0]: return True
        return False

    def set_d_banned(self, member: discord.Member, b: bool):
        """Set member is_d_banned to True"""

        self.c.execute('''
            UPDATE members SET is_d_banned=?, lifetime_d_bans=lifetime_d_bans+?
            WHERE discord_id=?;
        ''', (1 if b else 0, 1 if b else 0, member.id,))
        self.connection.commit()
