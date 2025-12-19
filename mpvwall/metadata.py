import subprocess
import json
import logging
from pathlib import Path
from typing import Optional, Dict

log = logging.getLogger("mpvwall.metadata")

def get_video_info(video_path: Path) -> Optional[Dict]:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path)
            ],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return None
        
        data = json.loads(result.stdout)
        
        video_stream = None
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream
                break
        
        if not video_stream:
            return None
        
        format_info = data.get("format", {})
        
        duration = float(format_info.get("duration", 0))
        duration_str = f"{int(duration//60)}:{int(duration%60):02d}" if duration > 0 else "?"
        
        size_bytes = int(format_info.get("size", 0))
        if size_bytes > 1024**3:
            size_str = f"{size_bytes / 1024**3:.1f}GB"
        elif size_bytes > 1024**2:
            size_str = f"{size_bytes / 1024**2:.1f}MB"
        else:
            size_str = f"{size_bytes / 1024:.1f}KB"
        
        fps_str = video_stream.get("r_frame_rate", "?")
        if "/" in fps_str:
            num, den = fps_str.split("/")
            fps = int(num) / int(den) if den != "0" else 0
            fps_str = f"{fps:.0f}" if fps > 0 else "?"
        
        return {
            "duration": duration_str,
            "width": video_stream.get("width", "?"),
            "height": video_stream.get("height", "?"),
            "resolution": f"{video_stream.get('width', '?')}x{video_stream.get('height', '?')}",
            "size": size_str,
            "fps": fps_str
        }
        
    except (subprocess.TimeoutExpired, json.JSONDecodeError, ValueError) as e:
        log.debug("Failed to get video info for %s: %s", video_path, str(e))
        return None
    except FileNotFoundError:
        log.debug("ffprobe not found, video metadata unavailable")
        return None

def format_video_info(info: Optional[Dict]) -> str:
    if not info:
        return ""
    
    parts = []
    if info.get("resolution"):
        parts.append(info["resolution"])
    if info.get("duration"):
        parts.append(info["duration"])
    if info.get("fps"):
        parts.append(f"{info['fps']}fps")
    if info.get("size"):
        parts.append(info["size"])
    
    return " | ".join(parts) if parts else ""
