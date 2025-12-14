import subprocess
import json

def get_monitors() -> list[str]:
    out = subprocess.check_output(
        ["hyprctl", "monitors", "-j"],
        text=True
    )
    data = json.loads(out)
    return [m["name"] for m in data]
