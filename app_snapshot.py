import os
import json
import subprocess


def get_active_apps():

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
    ignore_keys = [
        "Settings",
        "NVIDIA GeForce Overlay",
        "Windows Input Experience",
    ]

    for key in ignore_keys:
        json_obj.pop(key, None)

    script_dir = os.getcwd()
    json_file = os.path.join(script_dir, "active_apps.json")
    with open(json_file, "w") as f:
        json.dump(json_obj, f, indent=4)


    return json_obj


if __name__ == "__main__":

    get_active_apps()
