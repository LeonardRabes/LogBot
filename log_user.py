import discord
import asyncio
from typing import overload

class LogUser:
    def __init__(self, discord_user_id, steam_id_64):
        self.discord_user_id = discord_user_id
        self.steam_id_64 = steam_id_64
        self.latest_log_id = None


    def is_online(self):
        pass
    
    
    async def fetch_user(self, client):
        return await client.fetch_user(self.discord_user_id)

    def contains(self, discord_user_id, steam_id_64):
        return steam_id_64 == self.steam_id_64 or discord_user_id == self.discord_user_id


    def equals(self, user):
        return user.steam_id_64 == self.steam_id_64 and user.discord_user_id == self.discord_user_id
