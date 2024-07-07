import json
import os

CONFIG_PATH = "config/access.json"

def load_token():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as file:
            data = json.load(file)
            return data.get('token')
    return None

def save_token(token):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as file:
        json.dump({'token': token}, file)

def delete_token():
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
