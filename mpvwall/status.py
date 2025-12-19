import subprocess
import logging
import json

log = logging.getLogger("mpvwall.status")

def is_mpvpaper_running() -> bool:
    try:
        result = subprocess.run(
            ["pgrep", "-x", "mpvpaper"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        log.error("Failed to check mpvpaper status: %s", str(e))
        return False

def get_mpvpaper_pids() -> list[int]:
    try:
        result = subprocess.run(
            ["pgrep", "-x", "mpvpaper"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return [int(pid) for pid in result.stdout.strip().split("\n") if pid]
        return []
    except Exception as e:
        log.error("Failed to get mpvpaper PIDs: %s", str(e))
        return []

def check_hyprland_layers() -> dict:
    try:
        result = subprocess.run(
            ["hyprctl", "layers", "-j"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            mpvpaper_layers = []
            for monitor, monitor_data in data.items():
                if "levels" in monitor_data:
                    for level_name, layers in monitor_data["levels"].items():
                        for layer in layers:
                            if layer.get("namespace") == "mpvpaper":
                                mpvpaper_layers.append({
                                    "monitor": monitor,
                                    "level": level_name,
                                    "pid": layer.get("pid"),
                                    "size": f"{layer.get('w')}x{layer.get('h')}"
                                })
            return {
                "available": True,
                "layers": mpvpaper_layers,
                "count": len(mpvpaper_layers)
            }
    except Exception as e:
        log.warning("Failed to check Hyprland layers: %s", str(e))
    
    return {"available": False, "layers": [], "count": 0}
