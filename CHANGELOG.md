# Changelog

## [0.2.0] - 2025-12-16

### Added
- **Layer level configuration** - Choose between `background`, `bottom`, `top`, or `overlay` layers
- **Recursive search** - Press `R` to search for videos in subdirectories
- **Video metadata display** - Shows resolution, duration, file size, and FPS (requires `ffprobe`)
- **Pause/Resume control** - Press `P` to pause/resume via IPC (optional, disabled by default)
- **Status command** - `mpvwall --status` shows current wallpaper status and configuration
- **Help command** - `mpvwall --help` displays usage information
- **Enhanced error handling** - Better error messages and validation
- **mpvpaper log file** - Output saved to `~/.local/state/mpvwall/mpvpaper.log`
- **Dependency checking** - Validates that required tools are installed
- **Async notifications** - Non-blocking notifications in TUI
- **Metadata caching** - Fast navigation without lag

### Changed
- Improved logging with separate file for mpvpaper output
- Better UI with async notifications above Info line
- Default layer changed to `bottom` for better compatibility
- IPC support now optional (can cause issues with some layers)
- Non-blocking interface with smooth navigation
- Updated helpbar to show all available controls

### Fixed
- Proper error handling for missing files and commands
- Process validation after mpvpaper start
- Timeout handling for hyprctl commands
- Navigation lag from metadata loading
- Blocking notifications during file operations

## [0.1.0] - Initial Release

### Added
- Terminal UI for video wallpaper management
- Folder picker with curses interface
- Monitor selection (ALL or specific output)
- mpvpaper integration with fork mode
- Configuration persistence
- Autostart support with `--restore`
- NVIDIA GPU support
