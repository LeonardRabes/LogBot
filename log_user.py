import discord
import asyncio


class LogUser:
    def __init__(self, discord_user_id, steam_id_64):
        self.discord_user_id = discord_user_id
        self.steam_id_64 = steam_id_64
        self.latest_log_id = None


    def contains(self, discord_user_id, steam_id_64):
        return steam_id_64 == self.steam_id_64 or discord_user_id == self.discord_user_id


    def equals(self, user):
        return user.steam_id_64 == self.steam_id_64 and user.discord_user_id == self.discord_user_id
