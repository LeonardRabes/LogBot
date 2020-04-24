from bot import LogBot
from file_io import save_users, load_users, load_token


def main():
    token = load_token()
    bot = LogBot(token)
    bot.subscribed_users = load_users()

    bot.events.on_subscribe += save_users
    bot.events.on_unsubscribe += save_users

    bot.run()

if __name__ == "__main__":
    main()