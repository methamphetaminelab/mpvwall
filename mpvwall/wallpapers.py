from pathlib import Path
from typing import Union

VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".flv", ".wmv", ".m4v"}

def list_wallpapers(folder: Union[str, Path], recursive: bool = False) -> list[str]:
    """List video files in folder
    
    Args:
        folder: Path to folder
        recursive: If True, search recursively in subdirectories
    
    Returns:
        List of video filenames (relative paths if recursive)
    """
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        return []

    if recursive:
        # Recursive search - return relative paths
        videos = []
        for ext in VIDEO_EXTS:
            videos.extend(p.rglob(f"*{ext}"))
        
        # Convert to relative paths from base folder
        return sorted(
            str(f.relative_to(p)) for f in videos
        )
    else:
        # Non-recursive - just current folder
        return sorted(
            f.name for f in p.iterdir()
            if f.suffix.lower() in VIDEO_EXTS
        )
