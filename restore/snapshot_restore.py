import subprocess
import json
import os
import logging
import sys


def snapshot_restore():
    script_dir = os.getcwd()
    json_file = os.path.join(script_dir, "active_apps.json")
    with open(json_file, "r") as f:
        apps = json.load(f)
    for app in apps:
        subprocess.Popen(apps[app])


# main
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # logging path
    logging_path = os.path.join(os.getcwd(), "restore", "snapshot_restore_run.log")
    file_handler = logging.FileHandler(logging_path, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.info("Snapshot Backup Started")

    snapshot_restore()
    sys.exit(0)
