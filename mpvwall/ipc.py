import socket
import json
import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger("mpvwall.ipc")

IPC_SOCKET = Path("/tmp/mpvpaper.sock")

def send_command(command: str, args: list = None) -> Optional[dict]:
    if not IPC_SOCKET.exists():
        log.warning("IPC socket not found at %s", IPC_SOCKET)
        return None
    
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(str(IPC_SOCKET))
        
        request = {
            "command": [command] + (args or [])
        }
        
        sock.sendall((json.dumps(request) + "\n").encode())
        
        response = b""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk
            if b"\n" in chunk:
                break
        
        sock.close()
        
        if response:
            return json.loads(response.decode())
        
    except (socket.error, json.JSONDecodeError, FileNotFoundError) as e:
        log.debug("IPC command failed: %s", str(e))
        return None
    
    return None

def toggle_pause() -> bool:
    response = send_command("cycle", ["pause"])
    return response is not None

def get_pause_state() -> Optional[bool]:
    response = send_command("get_property", ["pause"])
    if response and "data" in response:
        return response["data"]
    return None
