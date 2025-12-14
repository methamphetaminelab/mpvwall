from pathlib import Path
from typing import Union

VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov"}

def list_wallpapers(folder: Union[str, Path]) -> list[str]:
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        return []

    return sorted(
        f.name for f in p.iterdir()
        if f.suffix.lower() in VIDEO_EXTS
    )
