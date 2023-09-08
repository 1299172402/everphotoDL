import os
import json

config_path = "config.json"

def init():
    if os.path.exists(config_path) == False:
        with open(config_path, "w", encoding = 'utf-8') as f:
            f.write(json.dumps({
                "token": "",
                "dl_path": "D:/EverPhoto",
                "share_dl_path": "D:/EverPhoto_Share",
                "get_meta": "todo",
            }, indent = 4, ensure_ascii = False))

def load(setting):
    with open(config_path, "r", encoding = "utf-8") as f:
        res = json.loads(f.read())
    if setting in res:
        return res[setting]
    else:
        return None

def save(setting, value):
    with open(config_path, "r", encoding = "utf-8") as f:
        res = json.loads(f.read())
    res[setting] = value
    with open(config_path, "w", encoding = "utf-8") as f:
        f.write(json.dumps(res, indent = 4, ensure_ascii = False))