from typing import overload

class LogUser:
    def __init__(self, discord_user, steam_id_64):
        self.discord_user = discord_user
        self.steam_id_64 = steam_id_64


    def is_online(self):
        pass
    

    def contains(self, discord_user, steam_id_64):
        return steam_id_64 == self.steam_id_64 and discord_user == self.discord_user


    def equals(self, user):
        return self.contains(user.discord_user, user.steam_id_64)