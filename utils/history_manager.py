import json
import os

def save_chat(doc_name, chat):

    os.makedirs("data", exist_ok=True)
    path = f"data/{doc_name}.json"

    with open(path, "w") as f:
        json.dump(chat, f)


def load_chat(doc_name):

    path = f"data/{doc_name}.json"

    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    return []