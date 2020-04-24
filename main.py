from bot import LogClient
from file_io import save_users, load_users, load_token

def main():
    token = load_token()
    client = LogClient(token)
    client.subscribed_users = load_users()

    client.events.on_subscribe += save_users
    client.events.on_unsubscribe += save_users

    client.run()

if __name__ == "__main__":
    main()