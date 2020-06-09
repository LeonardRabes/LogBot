from bot import LogBot
from file_io import save_users, load_users, load_secret
import discord

def main():
    client_token, bot_token, steam_api_key = load_secret()

    bot = LogBot(bot_token, steam_api_key)
    bot.subscribed_users = load_users()

    bot.events.on_subscribe += save_users
    bot.events.on_unsubscribe += save_users

    bot.run()

if __name__ == "__main__":
    main()