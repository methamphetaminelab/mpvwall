import subprocess
import logging
import os

log = logging.getLogger("mpvwall.mpvpaper")

def stop():
    log.info("Stopping mpvpaper")
    subprocess.run(["pkill", "mpvpaper"], stderr=subprocess.DEVNULL)

def start(wallpaper: str, output: str, options: str):
    stop()

    cmd = [
        "mpvpaper",
        "--layer", "bottom",
        "--fork",
        "--mpv-options", options,
        output.upper(),
        wallpaper,
    ]

    log.info("Starting mpvpaper: %s", " ".join(cmd))

    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=os.environ.copy(),
    )
