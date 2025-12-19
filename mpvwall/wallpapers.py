from pathlib import Path
from typing import Union

VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".flv", ".wmv", ".m4v"}

def list_wallpapers(folder: Union[str, Path], recursive: bool = False) -> list[str]:
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        return []

    if recursive:
        videos = []
        for ext in VIDEO_EXTS:
            videos.extend(p.rglob(f"*{ext}"))
        
        return sorted(
            str(f.relative_to(p)) for f in videos
        )
    else:
        return sorted(
            f.name for f in p.iterdir()
            if f.suffix.lower() in VIDEO_EXTS
        )
