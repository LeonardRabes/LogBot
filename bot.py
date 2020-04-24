import discord
import re
import asyncio
from tf_logs import get_player_log_list, get_latest_log_descr, get_log, summarize_log, get_latest_log
from log_user import LogUser
from events import Events


CMD_PREFIX = "!"


class LogClient(discord.Client):
    __events__ = ('on_subscribe', 'on_unsubscribe', )
    def __init__(self, token):
        super(LogClient, self).__init__()
        self.token = token
        self.subscribed_users = []
        self.events = Events()


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
            return False

        u = LogUser(discord_user_id, steam_id_64)
        self.subscribed_users.append(u)

        self.events.on_subscribe(self, u) #fire on_subscribe event

        return True


    def unsubscribe_user(self, discord_user_id=None, steam_id_64=None):
        u = self.get_subscribed_user(discord_user_id, steam_id_64)

        if u == None:
            return False

        self.subscribed_users.remove(u)

        self.events.on_unsubscribe(self, u) #fire on_unsubscribe event

        return True


    async def log_update_loop(self):
        while True:
            print("Log Update!")
            log_dict = {} #contains all logs of current update with log id as key
            for user in self.subscribed_users:
                
                log_list = get_player_log_list(user.steam_id_64)
                log_desc = get_latest_log_descr(log_list)

                if user.latest_log_id == None: #only run in the initial log request of user
                    user.latest_log_id = log_desc["id"]

                elif user.latest_log_id != log_desc["id"]:
                    user.latest_log_id = log_desc["id"]
                    fetch = asyncio.create_task(user.fetch_user(self))

                    if log_desc["id"] in log_dict:
                        log = log_dict[log_desc["id"]]
                    else:
                        log = get_log(log_desc)
                        log_dict[log_desc["id"]] = log

                    summary = summarize_log(log)
                    await fetch
                    user_obj = fetch.result()
                    await user_obj.dm_channel.send(summary)

                    print(f"Log[{user.latest_log_id}] sent to {user_obj.Name}, {user.steam_id_64}.")

            await asyncio.sleep(30)
            

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        #start log update loop
        asyncio.create_task(self.log_update_loop())


    async def on_message(self, message):
        if message.author == self.user:
            return

        print('Message from {0.author}: {0.content}'.format(message))
        #contains command
        if message.content[0] == CMD_PREFIX:
            #dm only
            if message.channel.id == message.author.dm_channel.id:
                #subscribe cmd
                if re.fullmatch("!subscribe +[0-9]{17} *", message.content) != None:
                    res = re.findall("[0-9]{17}", message.content)
                    steam_id = res[0]
                    succ = self.subscribe_user(message.author.id, steam_id)
                    if succ:
                        await message.channel.send("You are now subscribed and will receive Logs!")
                    else:
                        await message.channel.send("You could not be subscribed.")

                #unsubscribe cmd
                elif re.fullmatch("!unsubscribe *", message.content) != None:
                    succ = self.unsubscribe_user(message.author.id)
                    if succ:
                        await message.channel.send("You are now unsubscribed and will not receive Logs!")
                    else:
                        await message.channel.send("You could not be unsubscribed.")

                #latest cmd for subscribers
                elif re.fullmatch("!latest *", message.content) != None:
                    u = self.get_subscribed_user(message.author.id)

                    if u != None:
                        summary = get_latest_log(u.steam_id_64)
                        await message.channel.send(summary)

                #latest cmd without subscription
                elif re.fullmatch("!latest +[0-9]{17} *", message.content) != None:
                    res = re.findall("[0-9]{17}", message.content)
                    steam_id = res[0]
                    summary = get_latest_log(steam_id)
                    await message.channel.send(summary)

                #cmd not found
                else:
                    await message.channel.send("Command not found!")


                    

                    



