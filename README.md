# mpvwall 🎬

Terminal UI manager for **video wallpapers** using **mpvpaper** on Wayland.

`mpvwall` provides a simple curses-based interface to manage video wallpapers:
select a folder, choose a video, pick a monitor (or ALL), and apply it instantly.

The actual wallpaper process is handled by `mpvpaper`, which is launched in
**forked mode** — `mpvwall` itself does **not** stay running in the background.

> Tested primarily on **Hyprland** (Arch Linux), but should work on other Wayland
> compositors that support `layer-shell`.

## ✨ Features

- 🖥 Terminal UI (curses, no GUI dependencies)
- 🎞 Video wallpapers via `mpvpaper`
- 📂 Built-in folder picker
- 🔍 Recursive search in subdirectories
- 📊 Video metadata display (resolution, duration, size, FPS)
- 🖥 Monitor selection (ALL or per-output)
- 🛑 Start / Stop wallpaper
- ⏯️ Pause / Resume via IPC (optional)
- 🔁 Restore last wallpaper on login
- ⚙️ Configurable layer level (background, bottom, top, overlay)
- 💬 Async notifications (non-blocking)
- 🧠 NVIDIA-friendly (`gpu-context=wayland`)
- 🚀 No background daemon — `mpvpaper` is forked
- 📝 Detailed logging for debugging

## 📦 Requirements

### System
- Wayland compositor (tested on **Hyprland**)
- `mpv`
- `mpvpaper`
- `hyprctl` (from Hyprland)
- `ffprobe` (optional, for video metadata display)

### Python
- Python **>= 3.9**
- No external Python dependencies (standard library only)

## 🔧 Installation

### Arch Linux (AUR) — **recommended**

```bash
yay -S mpvwall-git
````

### From source

```bash
git clone https://github.com/methamphetaminelab/mpvwall
cd mpvwall
pip install -e .
```

This installs the `mpvwall` command into your environment.

## ▶ Usage

### Launch TUI

```bash
mpvwall
```

Controls:

* `↑` `↓` — select wallpaper
* `←` `→` — change monitor
* `Enter` — apply wallpaper
* `S` — stop wallpaper
* `P` — pause/resume playback (IPC)
* `F` — change folder
* `R` — toggle recursive search
* `Q` — quit

### Restore last wallpaper

```bash
mpvwall --restore
```

Restores:

* last selected wallpaper
* selected monitor
* mpv options

Useful for autostart.

### Check status

```bash
mpvwall --status
```

Shows:
* Whether mpvpaper is running
* Current wallpaper configuration
* Hyprland layer information
* Log file locations

## ⚙ Configuration

Configuration file:

```text
~/.config/mpvwall/config.json
```

Example:

```json
{
  "wallpapers_dir": "/home/user/Wallpapers",
  "selected": "example.mp4",
  "output": "ALL",
  "mpv_options": "loop no-audio gpu-context=wayland",
  "layer": "bottom",
  "recursive": false,
  "enable_ipc": false
}
```

**Options:**
- `layer`: Layer level - `bottom` (recommended), `background`, `top`, or `overlay`
  - Use `bottom` for best compatibility
  - `background` may not work with IPC enabled
- `recursive`: Search for videos in subdirectories
- `enable_ipc`: Enable IPC socket for pause/resume control (disable if wallpapers don't start)

## 🚀 Autostart (Hyprland)

Add to `~/.config/hypr/hyprland.conf`:

```ini
exec-once = mpvwall --restore
```

If wallpapers start too early:

```ini
exec-once = sleep 1 && mpvwall --restore
```

⚠️ **Important**
Do **not** run other wallpaper managers (`swww`, `hyprpaper`, `waypaper`)
at the same time — they will conflict with `mpvpaper`.

## 🧪 Troubleshooting

### Wallpaper does not appear

* Make sure no other wallpaper daemon is running:

  ```bash
  pkill swww
  pkill hyprpaper
  ```

* Check logs:

  ```bash
  ~/.local/state/mpvwall/mpvwall.log
  ~/.local/state/mpvwall/mpvpaper.log
  ```

  The `mpvpaper.log` contains output from mpvpaper itself, which may reveal
  why the wallpaper stops unexpectedly.

### NVIDIA users

Recommended mpv options (default):

```text
loop no-audio gpu-context=wayland
```

## 📜 Logging

Logs are written to:

```text
~/.local/state/mpvwall/mpvwall.log   (application log)
~/.local/state/mpvwall/mpvpaper.log  (mpvpaper output)
```

Enable debug logging:

```bash
mpvwall --debug
```

## 🆘 Help

Show help message:

```bash
mpvwall --help
```

## ❤️ Acknowledgements

* [`mpv`](https://mpv.io/)
* [`mpvpaper`](https://github.com/GhostNaN/mpvpaper)
* Hyprland community