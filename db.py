import sqlite3
import discord


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('discord.db')
        self.c = self.connection.cursor()

    def init(self):
        """"Make tables for db"""

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                discriminator TEXT NOT NULL,
                discord_id INTEGER,
                joined_guild DATE NOT NULL,
                points INTEGER NOT NULL,
                lifetime_points INTEGER NOT NULL,
                warn_level INTEGER NOT NULL
            );
        ''')
        self.connection.commit()

    def delete_all(self, table: str):
        """Drop all data in table"""

        self.c.execute(f'''
            DELETE FROM {table};
        ''')
        self.connection.commit()

    def new_member(self, member: discord.Member):
        """Create new entry in members table of member"""

        self.c.execute('''
            INSERT INTO members
            (name, discriminator, discord_id, joined_guild, points,
                lifetime_points, warn_level)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        ''', (
            member.name,
            member.discriminator,
            member.id,
            member.joined_at,
            0,
            0,
            0
        ))
        self.connection.commit()

    def member_exists(self, member: discord.Member):
        """Return if member exists in db referenced from discord.Member"""

        self.c.execute('''
            SELECT 1 from members WHERE discord_id=?;
        ''', (member.id,))

        if not self.c.fetchone(): return False
        return True

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

    def get_member(self, member: discord.Member) -> dict:
        """Return member from db referenced from discord.Member"""

        self.c.execute('''
            SELECT * FROM members WHERE discord_id=?;
        ''', (member.id,))

        member = self.c.fetchone()
        member = {
            'id': member[0],
            'name': member[1],
            'discriminator': member[2],
            'discord_id': member[3],
            'joined_guild': member[4],
            'points': member[5],
            'lifetime_points': member[6],
            'warn_level': member[7]
        }

        return member

    def get_top_points(self) -> list:
        """Return a sorted list of the top 10 members sorted by points"""

        self.c.execute('''
            SELECT discord_id, points FROM members ORDER BY points DESC LIMIT 10;
        ''')

        return self.c.fetchall()

    def add_warn(self, member: discord.Member):
        """Add warning to member"""

        self.c.execute('''
            UPDATE members SET warn_level=warn_level+1 WHERE discord_id=?;
        ''', (member.id,))
        self.connection.commit()

    def reset_warn(self, member: discord.Member):
        """Reset warning level of member"""

        self.c.execute('''
            UPDATE members SET warn_level=0 WHERE discord_id=?;
        ''', (member.id,))
        self.connection.commit()
