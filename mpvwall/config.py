from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".config/mpvwall"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT = {
    "wallpapers_dir": "",
    "selected": "",
    "output": "ALL",
    "mpv_options": "loop no-audio gpu-context=wayland vid=1 hwdec=auto-safe",
    "layer": "bottom",
    "recursive": False,
    "enable_ipc": False
}

def load():
    if not CONFIG_FILE.exists():
        return DEFAULT.copy()
    return {**DEFAULT, **json.loads(CONFIG_FILE.read_text())}

def save(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
