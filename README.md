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
- 🖥 Monitor selection (ALL or per-output)
- 🛑 Start / Stop wallpaper
- 🔁 Restore last wallpaper on login
- 🧠 NVIDIA-friendly (`gpu-context=wayland`)
- 🚀 No background daemon — `mpvpaper` is forked

## 📦 Requirements

### System
- Wayland compositor (tested on **Hyprland**)
- `mpv`
- `mpvpaper`
- `hyprctl` (from Hyprland)

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
* `F` — change folder
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
  "mpv_options": "loop no-audio gpu-context=wayland"
}
```

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
  ```

### NVIDIA users

Recommended mpv options (default):

```text
loop no-audio gpu-context=wayland
```

## 📜 Logging

Logs are written to:

```text
~/.local/state/mpvwall/mpvwall.log
```

Enable debug logging:

```bash
mpvwall --debug
```

## ❤️ Acknowledgements

* [`mpv`](https://mpv.io/)
* [`mpvpaper`](https://github.com/GhostNaN/mpvpaper)
* Hyprland community