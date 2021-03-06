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
                points INTEGER NOT NULL
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
            INSERT INTO members (name, discriminator, discord_id, joined_guild, points)
            VALUES (?, ?, ?, ?, ?);
        ''', (
            member.name,
            member.discriminator,
            member.id,
            member.joined_at,
            0,
        ))
        self.connection.commit()
    
    def member_exists(self, member: discord.Member):
        """Return if member exists in db referenced from discord.Member"""

        self.c.execute('''
            SELECT 1 from members WHERE discord_id=?
        ''', (member.id,))

        if not self.c.fetchone(): return False
        return True
    
    def add_points(self, member: discord.Member, points: int):
        """Add points to discord member"""

        self.c.execute('''
            UPDATE members SET points=points+? WHERE discord_id=?
        ''', (points, member.id,))
        self.connection.commit()
