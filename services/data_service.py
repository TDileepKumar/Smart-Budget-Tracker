import json
import os

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"transactions": []}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or "transactions" not in data:
                return {"transactions": []}
            if not isinstance(data["transactions"], list):
                return {"transactions": []}
            return data
    except (json.JSONDecodeError, OSError):
        return {"transactions": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)