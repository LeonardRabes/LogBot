import discord
import re
import asyncio
from tf_logs import get_player_log_lists, get_latest_log_descr, get_log, summarize_log
from log_user import LogUser


class LogClient(discord.Client):
    def __init__(self, token):
        super(LogClient, self).__init__()
        self.token = token
        self.subscribed_users = []
        self.log_loop = asyncio.get_event_loop()


    def run(self):
        super(LogClient, self).run(self.token)


    def get_subscribed_user(self, discord_user, steam_id_64):
        for u in self.subscribed_users:
            if u.contains(discord_user, steam_id_64):
                return u
        return None


    def subscribe_user(self, discord_user, steam_id_64):
        if self.get_subscribed_user(discord_user, steam_id_64) == None:
            return False

        u = LogUser(discord_user, steam_id_64)
        self.subscribed_users.append(u)

        return True


    def unsubscribe_user(self, discord_user, steam_id_64):
        u = self.get_subscribed_user(discord_user, steam_id_64)

        if u == None:
            return False

        self.subscribed_users.remove(u)
        return True


    async def log_update_loop(self):
        while True:
            await asyncio.sleep(1)
            

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        #start log update loop
        asyncio.ensure_future(self.log_update_loop())


    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

