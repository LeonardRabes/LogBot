import discord
import re
import asyncio
from tf_logs import get_player_log_lists, get_latest_log_descr, get_log, summarize_log
from log_user import LogUser


CMD_PREFIX = "!"


class LogClient(discord.Client):
    def __init__(self, token):
        super(LogClient, self).__init__()
        self.token = token
        self.subscribed_users = []
        self.log_loop = asyncio.get_event_loop()


    def run(self):
        super(LogClient, self).run(self.token)


    def get_subscribed_user(self, discord_user_id=None, steam_id_64=None):
        for u in self.subscribed_users:
            if u.contains(discord_user_id, steam_id_64):
                return u
        return None


    def subscribe_user(self, discord_user_id, steam_id_64):
        u = self.get_subscribed_user(discord_user_id, steam_id_64)
        if u != None:
            return u

        u = LogUser(discord_user_id, steam_id_64)
        self.subscribed_users.append(u)

        return u


    def unsubscribe_user(self, discord_user_id=None, steam_id_64=None):
        u = self.get_subscribed_user(discord_user_id, steam_id_64)

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
        if message.author == self.user:
            return

        print('Message from {0.author}: {0.content}'.format(message))

        if message.content[0] == CMD_PREFIX:
            #dm only
            if message.channel.id == message.author.dm_channel.id:
                if "subscribe" in message.content:
                    res = re.findall("[0-9]{17}", message.content)
                    if len(res) == 1:
                        steam_id = res[0]
                        u = self.subscribe_user(message.author.id, steam_id)
                    else:
                        print("Wrong Cmd Format!")

                    

                    



