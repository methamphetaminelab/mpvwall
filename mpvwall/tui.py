import curses
from pathlib import Path

from .config import load, save
from .wallpapers import list_wallpapers
from .mpvpaper import start, stop
from .filepicker import pick_directory
from .monitors import get_monitors

def run():
    curses.wrapper(main)

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    cfg = load()

    if not cfg["wallpapers_dir"]:
        folder = pick_directory(stdscr)
        if not folder:
            return
        cfg["wallpapers_dir"] = str(folder)
        save(cfg)

    folder = Path(cfg["wallpapers_dir"])
    wallpapers = list_wallpapers(folder)
    idx = 0

    monitors = ["ALL"] + get_monitors()
    mon_idx = monitors.index(cfg["output"]) if cfg["output"] in monitors else 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, 2, "mpvwall", curses.A_BOLD)
        stdscr.addstr(2, 2, f"Folder: {folder}")
        stdscr.addstr(4, 2, "Wallpapers:")

        max_rows = h - 8
        offset = max(0, idx - max_rows + 1)

        for i, name in enumerate(wallpapers[offset:offset + max_rows]):
            real = offset + i
            attr = curses.A_REVERSE if real == idx else curses.A_NORMAL
            stdscr.addstr(5 + i, 4, name[:w - 8], attr)

        status = f"Wallpaper: {cfg['selected'] or '-'} | Output: {monitors[mon_idx]}"
        helpbar = "[↑↓] Select  [←→] Monitor  [Enter] Apply  [S] Stop  [F] Folder  [Q] Quit"

        stdscr.addstr(h - 2, 2, status[:w - 4], curses.A_DIM)
        stdscr.addstr(h - 1, 2, helpbar[:w - 4], curses.A_DIM)

        stdscr.refresh()
        key = stdscr.getch()

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
            start(str(folder / cfg["selected"]), cfg["output"], cfg["mpv_options"])
        elif key in (ord("s"), ord("S")):
            stop()
        elif key in (ord("f"), ord("F")):
            new = pick_directory(stdscr, folder)
            stdscr.clear()
            stdscr.refresh()
            if new:
                folder = new
                cfg["wallpapers_dir"] = str(new)
                save(cfg)
                wallpapers = list_wallpapers(folder)
                idx = 0
        elif key in (ord("q"), ord("Q")):
            break
