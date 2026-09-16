import json
import os

filename = "config.json"

default_config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "settings": {
        "theme": "dark",
        "notifications": True
    }
}

if not os.path.exists(filename):
    with open(filename, "w") as file:
        json.dump(default_config, file, indent=4)

with open(filename, "r") as file:
    config = json.load(file)

current_theme = config["settings"]["theme"]
print(f"Current Theme: {current_theme}")

config["settings"]["theme"] = "light"

with open(filename, "w") as file:
    json.dump(config, file, indent=4)