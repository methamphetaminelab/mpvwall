import curses
import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger("mpvwall.filepicker")

def pick_directory(stdscr, start_path=None) -> Optional[Path]:
    curses.curs_set(0)
    stdscr.keypad(True)

    cwd = Path(start_path or Path.home()).resolve()
    idx = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        max_rows = h - 6
        offset = max(0, idx - max_rows + 1)

        stdscr.addstr(1, 2, "Select wallpapers folder", curses.A_BOLD)
        stdscr.addstr(2, 2, f"Path: {cwd}")

        entries = [".."] + sorted(
            [p.name for p in cwd.iterdir() if p.is_dir()]
        )

        for i, name in enumerate(entries[offset:offset + max_rows]):
            real = offset + i
            attr = curses.A_REVERSE if real == idx else curses.A_NORMAL
            stdscr.addstr(4 + i, 4, name[:w - 8], attr)

        stdscr.addstr(h - 2, 2, "[Enter] Open  [Space] Select  [Q] Cancel")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and idx > 0:
            idx -= 1
        elif key == curses.KEY_DOWN and idx < len(entries) - 1:
            idx += 1
        elif key in (10, 13):
            name = entries[idx]
            cwd = cwd.parent if name == ".." else cwd / name
            idx = 0
        elif key == ord(" "):
            log.info("Directory selected: %s", cwd)
            return cwd
        elif key in (ord("q"), ord("Q")):
            return None
