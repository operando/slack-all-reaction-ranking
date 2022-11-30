from collections import defaultdict

import requests

# ここにtokne入れると動く
headers = {'Authorization': 'Bearer XXX'}
user = "XXXX"


def get_reactions_list(param):
    param.update(limit=1000)
    r = requests.get("https://slack.com/api/reactions.list", params=param, headers=headers)
    json = r.json()
    return json


def sort(emojis):
    emojis_sorted = sorted(emojis.items(), key=lambda x: x[1], reverse=True)

    return emojis_sorted


def save_file(emojis):
    f = open('result.txt', 'w')
    for i, (k, v) in enumerate(emojis):
        f.write(f"{str(i + 1)}位 : :{k}: {v}回\n")
    f.close()


if __name__ == '__main__':
    emojis = defaultdict(lambda: 0)
    has_next = True
    cursor = ""
    while has_next:
        reactions_list = get_reactions_list({"cursor": cursor, "user": user})
        for items in reactions_list["items"]:
            for reactions in (
                    items["message"]["reactions"] if items["type"] == "message" else items["file"]["reactions"]):
                if user not in reactions["users"]:
                    continue
                emojis[reactions["name"]] += 1
        cursor = reactions_list["response_metadata"]["next_cursor"]
        has_next = cursor != ""
    emojis_sorted = sort(emojis)
    save_file(emojis_sorted)
