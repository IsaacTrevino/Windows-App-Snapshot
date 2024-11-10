import subprocess
import json
import os

def on_startup(apps: dict):
    for app in apps:
        print(apps[app])
        subprocess.Popen(apps[app])


# main
if __name__ == "__main__":
    script_dir = os.getcwd()
    json_file = os.path.join(script_dir, "active_apps.json")
    with open("active_apps.json", "r") as f:
        apps = json.load(f)

    on_startup(apps)