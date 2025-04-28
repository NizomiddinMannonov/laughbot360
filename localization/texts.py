import json
import os

file_path = os.path.join(os.path.dirname(__file__), "texts.json")

with open(file_path, "r", encoding="utf-8") as f:
    texts = json.load(f)
