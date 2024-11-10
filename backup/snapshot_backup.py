import os
import json
import subprocess
import logging
import sys


def snapshot_backup():

    cmd = "Get-Process | Where-Object { $_.MainWindowTitle } | Select-Object MainWindowTitle, Path | Format-Table -AutoSize -Wrap"
    process = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    output = output.decode("utf-8").splitlines()
    output = output[3:]
    output = list(filter(None, output))
    for i in range(len(output)):
        if output[i].startswith(" "):
            output[i - 1] += output[i].strip()
            output[i] = ""

    output = list(filter(None, output))
    output = [x.strip() for x in output]
    output = [x for x in output if len(x) > 1]

    json_obj: dict = {}
    for i in range(len(output)):
        output[i] = output[i].split("C:\\")
        output[i] = [x for x in output[i] if x]
    for i in range(len(output)):
        if len(output[i]) > 1:
            json_obj[output[i][0].strip().split("-")[-1].strip()] = (
                "C:\\" + output[i][1].strip()
            )
    # remove strings with more than 1 spaces for path and reduce to single space  C:\Users\isaac\AppData\Local\Programs\Microsoft VS      Code\Code.exe to C:\Users\isaac\AppData\Local\Programs\Microsoft VS Code\Code.exe
    for key in json_obj:
        json_obj[key] = " ".join(json_obj[key].split())

    ignore_keys = [
        "Settings",
        "NVIDIA GeForce Overlay",
        "Windows Input Experience",
        "Mail",
    ]

    for key in ignore_keys:
        json_obj.pop(key, None)

    script_dir = os.getcwd()
    json_file = os.path.join(script_dir, "active_apps.json")
    with open(json_file, "w") as f:
        json.dump(json_obj, f, indent=4)

    return json_obj


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    # logging path
    logging_path = os.path.join(os.getcwd(), "backup", "snapshot_backup_run.log")
    file_handler = logging.FileHandler(logging_path, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.info("Snapshot Backup Started")

    snapshot_backup()
    sys.exit(0)
