
import urllib.request
import json
import re


def get_steam_id_64(profile_url, api_key):
    if re.fullmatch("https://steamcommunity.com/id/[a-zA-Z0-9]+/* *", profile_url) != None:
        try:
            vanityurl = re.sub("https://steamcommunity.com/id/", "", profile_url).replace("/", "").replace(" ", "")
            url_str = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?vanityurl={vanityurl}&key={api_key}"

            with urllib.request.urlopen(url_str) as url:
                data = json.loads(url.read().decode())
            return data["response"]["steamid"]
        except Exception as e:
            print(str(e))

    elif re.fullmatch("https://steamcommunity.com/profiles/[0-9]{17}/* *", profile_url) != None:
        return re.findall("[0-9]{17}", profile_url)[0]

    return None
