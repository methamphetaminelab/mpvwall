import subprocess
import logging
import os
import shutil
from pathlib import Path

log = logging.getLogger("mpvwall.mpvpaper")

MPVPAPER_LOG = Path.home() / ".local/state/mpvwall/mpvpaper.log"

def stop():
    log.info("Stopping mpvpaper")
    result = subprocess.run(["pkill", "mpvpaper"], stderr=subprocess.PIPE, text=True)
    if result.returncode != 0 and result.returncode != 1:
        log.warning("pkill mpvpaper returned %d: %s", result.returncode, result.stderr)

def start(wallpaper: str, output: str, options: str, layer: str = "bottom", enable_ipc: bool = False):
    if not shutil.which("mpvpaper"):
        log.error("mpvpaper not found! Please install it first.")
        raise FileNotFoundError("mpvpaper is not installed")
    
    if not Path(wallpaper).exists():
        log.error("Wallpaper file not found: %s", wallpaper)
        raise FileNotFoundError(f"Wallpaper not found: {wallpaper}")
    
    stop()

    mpv_opts = options
    if enable_ipc:
        ipc_socket = "/tmp/mpvpaper.sock"
        if os.path.exists(ipc_socket):
            try:
                os.remove(ipc_socket)
            except OSError:
                pass
        mpv_opts = f"{options} input-ipc-server={ipc_socket}"
        log.info("IPC enabled at %s", ipc_socket)

    cmd = [
        "mpvpaper",
        "--layer", layer,
        "--fork",
        "--mpv-options", mpv_opts,
        output.upper(),
        wallpaper,
    ]

    log.info("Starting mpvpaper: %s", " ".join(cmd))

    MPVPAPER_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(MPVPAPER_LOG, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n{'='*80}\n")
            log_file.write(f"Starting mpvpaper at {subprocess.check_output(['date'], text=True).strip()}\n")
            log_file.write(f"Command: {' '.join(cmd)}\n")
            log_file.write(f"{'='*80}\n")
            
            process = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                env=os.environ.copy(),
            )
            
            log.info("mpvpaper started (PID: %d)", process.pid)
                
    except Exception as e:
        log.error("Failed to start mpvpaper: %s", str(e))
        raise
