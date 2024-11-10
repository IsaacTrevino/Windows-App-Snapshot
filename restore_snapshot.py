import subprocess


def on_startup(apps: dict):
    for app in apps:
        print(apps[app])
        subprocess.Popen(apps[app])
