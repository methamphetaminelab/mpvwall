import subprocess
import json
import logging
import shutil

log = logging.getLogger("mpvwall.monitors")

def get_monitors() -> list[str]:
    # Check if hyprctl is available
    if not shutil.which("hyprctl"):
        log.error("hyprctl not found! Is Hyprland running?")
        raise FileNotFoundError("hyprctl is not available")
    
    try:
        out = subprocess.check_output(
            ["hyprctl", "monitors", "-j"],
            text=True,
            stderr=subprocess.PIPE,
            timeout=5
        )
        data = json.loads(out)
        monitors = [m["name"] for m in data]
        log.info("Detected monitors: %s", monitors)
        return monitors
    except subprocess.TimeoutExpired:
        log.error("hyprctl timed out")
        raise RuntimeError("hyprctl command timed out")
    except subprocess.CalledProcessError as e:
        log.error("hyprctl failed: %s", e.stderr)
        raise RuntimeError(f"hyprctl failed: {e.stderr}")
    except (json.JSONDecodeError, KeyError) as e:
        log.error("Failed to parse hyprctl output: %s", str(e))
        raise RuntimeError(f"Failed to parse monitor data: {str(e)}")
