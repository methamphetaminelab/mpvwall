import sys
import logging

from mpvwall.log import setup_logging
from mpvwall.autostart import restore
from mpvwall.tui import run
from mpvwall.status import is_mpvpaper_running, get_mpvpaper_pids, check_hyprland_layers
from mpvwall.config import load

def print_help():
    help_text = """
mpvwall - Terminal UI manager for mpvpaper video wallpapers

Usage:
    mpvwall              Launch the TUI to select and apply wallpapers
    mpvwall --restore    Restore last selected wallpaper (for autostart)
    mpvwall --status     Check if wallpaper is running
    mpvwall --debug      Enable debug logging
    mpvwall --help       Show this help message

Controls (in TUI):
    ↑ ↓         Select wallpaper
    ← →         Change monitor
    Enter       Apply wallpaper
    S           Stop wallpaper
    F           Change folder
    Q           Quit

Configuration:
    ~/.config/mpvwall/config.json

Logs:
    ~/.local/state/mpvwall/mpvwall.log
    ~/.local/state/mpvwall/mpvpaper.log (mpvpaper output)

Requirements:
    - mpvpaper (video wallpaper daemon)
    - hyprctl (from Hyprland)
    - mpv (media player)

For more information: https://github.com/methamphetaminelab/mpvwall
"""
    print(help_text)

def print_status():
    """Print current wallpaper status"""
    cfg = load()
    
    print("=== mpvwall Status ===\n")
    
    # Check if mpvpaper is running
    running = is_mpvpaper_running()
    pids = get_mpvpaper_pids()
    
    if running:
        print(f"✓ mpvpaper is running (PID: {', '.join(map(str, pids))})")
    else:
        print("✗ mpvpaper is not running")
    
    # Show current config
    print(f"\nCurrent wallpaper: {cfg.get('selected', 'None')}")
    print(f"Folder: {cfg.get('wallpapers_dir', 'Not set')}")
    print(f"Output: {cfg.get('output', 'ALL')}")
    print(f"MPV options: {cfg.get('mpv_options', 'default')}")
    
    # Check Hyprland layers
    layer_info = check_hyprland_layers()
    if layer_info["available"]:
        if layer_info["count"] > 0:
            print(f"\n✓ Found {layer_info['count']} mpvpaper layer(s) in Hyprland")
            for layer in layer_info["layers"]:
                print(f"  - Monitor: {layer['monitor']}, Level: {layer['level']}")
        else:
            print("\n⚠️  No mpvpaper layers found in Hyprland (wallpaper may not be visible)")
    
    # Show logs location
    print(f"\nLogs:")
    print(f"  ~/.local/state/mpvwall/mpvwall.log")
    print(f"  ~/.local/state/mpvwall/mpvpaper.log")

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        return
    
    if "--status" in sys.argv:
        print_status()
        return
    
    DEBUG = "--debug" in sys.argv

    setup_logging(debug=DEBUG)
    log = logging.getLogger("mpvwall")

    log.info("mpvwall started")

    try:
        if "--restore" in sys.argv:
            restore()
        else:
            run()
    except KeyboardInterrupt:
        log.info("Interrupted by user")
    except Exception as e:
        log.exception("Fatal error: %s", str(e))
        print(f"\n❌ Error: {str(e)}")
        print(f"Check logs: ~/.local/state/mpvwall/mpvwall.log")
        sys.exit(1)

    log.info("mpvwall exited")


if __name__ == "__main__":
    main()
