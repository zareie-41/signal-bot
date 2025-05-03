import json

def load_coins():
    with open('config/coins.json', 'r') as f:
        return json.load(f)
