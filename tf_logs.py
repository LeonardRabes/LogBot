import urllib.request
import json


def get_player_log_list(steam_id_64):
    with urllib.request.urlopen(f"http://logs.tf/api/v1/log?player={steam_id_64}&limit=5") as url:
        data = json.loads(url.read().decode())

    return data


def get_latest_log_descr(player_log_list):
    return player_log_list["logs"][0]


def get_log(log_descr):
    with urllib.request.urlopen(f"http://logs.tf/json/{log_descr['id']}") as url:
        data = json.loads(url.read().decode())

    return data


def summarize_log(log):
    return log["info"]["title"]


def get_latest_log(steam_id_64):
    log_list = get_player_log_list(steam_id_64)
    log_desc = get_latest_log_descr(log_list)
    log = get_log(log_desc)
    summary = summarize_log(log)

    return summary