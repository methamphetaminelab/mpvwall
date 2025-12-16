import curses
from pathlib import Path
import logging
import time

from .config import load, save
from .wallpapers import list_wallpapers
from .mpvpaper import start, stop
from .filepicker import pick_directory
from .monitors import get_monitors
from .metadata import get_video_info, format_video_info
from .ipc import toggle_pause

log = logging.getLogger("mpvwall.tui")

def run():
    curses.wrapper(main)

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(100)

    notification_msg = ""
    notification_time = 0
    notification_duration = 0

    def show_notification(message: str, duration: float = 1.0):
        nonlocal notification_msg, notification_time, notification_duration
        notification_msg = message
        notification_time = time.time()
        notification_duration = duration

    cfg = load()

    if not cfg["wallpapers_dir"]:
        stdscr.timeout(-1)
        folder = pick_directory(stdscr)
        stdscr.timeout(100)
        if not folder:
            return
        cfg["wallpapers_dir"] = str(folder)
        save(cfg)

    folder = Path(cfg["wallpapers_dir"])
    wallpapers = list_wallpapers(folder, cfg.get("recursive", False))
    idx = 0
    
    metadata_cache = {}

    try:
        monitors = ["ALL"] + get_monitors()
    except Exception as e:
        log.error("Failed to get monitors: %s", str(e))
        monitors = ["ALL"]
        show_notification(f"Warning: Could not detect monitors ({str(e)})", 3)
    
    mon_idx = monitors.index(cfg["output"]) if cfg["output"] in monitors else 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, 2, "mpvwall", curses.A_BOLD)
        rec_indicator = " [RECURSIVE]" if cfg.get("recursive", False) else ""
        stdscr.addstr(2, 2, f"Folder: {folder}{rec_indicator}")
        stdscr.addstr(4, 2, "Wallpapers:")

        max_rows = h - 10
        offset = max(0, idx - max_rows + 1)

        for i, name in enumerate(wallpapers[offset:offset + max_rows]):
            real = offset + i
            attr = curses.A_REVERSE if real == idx else curses.A_NORMAL
            stdscr.addstr(5 + i, 4, name[:w - 8], attr)

        if wallpapers and idx < len(wallpapers):
            selected_name = wallpapers[idx]
            if selected_name not in metadata_cache:
                selected_path = folder / selected_name
                metadata_cache[selected_name] = get_video_info(selected_path)
            
            info = metadata_cache[selected_name]
            if info:
                info_str = format_video_info(info)
                stdscr.addstr(h - 3, 2, f"Info: {info_str}"[:w - 4], curses.A_DIM)

        current_time = time.time()
        if notification_msg and (current_time - notification_time) < notification_duration:
            stdscr.addstr(h - 4, 2, notification_msg[:w - 4], curses.A_REVERSE)

        status = f"Wallpaper: {cfg['selected'] or '-'} | Output: {monitors[mon_idx]}"
        helpbar = "[↑↓] Select [←→] Monitor [Enter] Apply [S] Stop [P] Pause [F] Folder [R] Rec [Q] Quit"

        stdscr.addstr(h - 2, 2, status[:w - 4], curses.A_DIM)
        stdscr.addstr(h - 1, 2, helpbar[:w - 4], curses.A_DIM)

        stdscr.refresh()
        key = stdscr.getch()

        if key == -1:
            continue
        
        if key == curses.KEY_UP and idx > 0:
            idx -= 1
        elif key == curses.KEY_DOWN and idx < len(wallpapers) - 1:
            idx += 1
        elif key == curses.KEY_LEFT:
            mon_idx = (mon_idx - 1) % len(monitors)
            cfg["output"] = monitors[mon_idx]
            save(cfg)
        elif key == curses.KEY_RIGHT:
            mon_idx = (mon_idx + 1) % len(monitors)
            cfg["output"] = monitors[mon_idx]
            save(cfg)
        elif key in (10, 13) and wallpapers:
            cfg["selected"] = wallpapers[idx]
            save(cfg)
            try:
                start(
                    str(folder / cfg["selected"]), 
                    cfg["output"], 
                    cfg["mpv_options"], 
                    cfg.get("layer", "bottom"),
                    cfg.get("enable_ipc", False)
                )
                show_notification("✓ Wallpaper applied successfully!", 1)
            except FileNotFoundError as e:
                log.error("Failed to start wallpaper: %s", str(e))
                show_notification(f"Error: {str(e)}", 3)
            except Exception as e:
                log.error("Unexpected error: %s", str(e))
                show_notification(f"Error: {str(e)}", 3)
        elif key in (ord("s"), ord("S")):
            try:
                stop()
                show_notification("✓ Wallpaper stopped", 1)
            except Exception as e:
                log.error("Failed to stop wallpaper: %s", str(e))
                show_notification(f"Error: {str(e)}", 3)
        elif key in (ord("p"), ord("P")):
            if toggle_pause():
                show_notification("⏯ Toggled pause", 1)
            else:
                show_notification("⚠️ IPC not available (restart wallpaper)", 2)
        elif key in (ord("f"), ord("F")):
            stdscr.timeout(-1)
            new = pick_directory(stdscr, folder)
            stdscr.timeout(100)
            stdscr.clear()
            stdscr.refresh()
            if new:
                folder = new
                cfg["wallpapers_dir"] = str(new)
                save(cfg)
                wallpapers = list_wallpapers(folder, cfg.get("recursive", False))
                idx = 0
                metadata_cache.clear()
        elif key in (ord("r"), ord("R")):
            cfg["recursive"] = not cfg.get("recursive", False)
            save(cfg)
            wallpapers = list_wallpapers(folder, cfg["recursive"])
            idx = 0
            metadata_cache.clear()
            mode = "enabled" if cfg["recursive"] else "disabled"
            show_notification(f"Recursive mode {mode}", 1)
        elif key in (ord("q"), ord("Q")):
            break
