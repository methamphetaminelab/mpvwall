from pathlib import Path
import logging

from .config import load
from .mpvpaper import start

log = logging.getLogger("mpvwall.restore")

def restore():
    cfg = load()

    if not cfg["wallpapers_dir"] or not cfg["selected"]:
        return

    path = Path(cfg["wallpapers_dir"]) / cfg["selected"]
    if not path.exists():
        return

    start(str(path), cfg["output"], cfg["mpv_options"])
