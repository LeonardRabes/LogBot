import urllib.request, json 


def get_player_log_lists(steam_ids):
    ids = ""
    for i, sid in enumerate(steam_ids):
        ids += str(sid)
        if i < len(steam_ids) - 1:
            ids += ","

    with urllib.request.urlopen(f"http://logs.tf/api/v1/log?player={ids}") as url:
        data = json.loads(url.read().decode())

    return data


def get_latest_log_descr(player_log_list):
    pass


def get_log(log_descr):
    pass


def summarize_log(log):
    pass