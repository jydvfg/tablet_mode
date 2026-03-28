# Tablet Mode Manager v1.0

System tray utility for 2-in-1 laptops to toggle tablet mode (disabling keyboard/touchpad) and rotating the screen. I created this solution for my MSI Prestige 14 AI+ after installing Ubuntu 26.04 LTS (dev branch) and realizing lid sensors for screen flipping and accelerometer weren't working.

## Features

- **Device Toggling:** System tray icon (green = enabled, red = disabled).
- **One-Click Disabling:** Quickly disables both internal keyboard and touchpad.
- **Screen Rotation:** Right/Left screen rotation support via context menu.
- **Wayland-native:** Uses sysfs inhibition and Mutter DBus bindings. No X11 dependencies.

## Requirements

- Python 3
- `pystray`, `python3-pil`, `python3-pydbus`
- `gnome-randr` (Rust binary)
- udev (for sysfs file permission persistence)

## Installation

1. Install system dependencies:
`sudo apt install python3-pystray python3-pil python3-pydbus`

2. Set udev rules for persistent sysfs permissions:
`sudo cp 99-tablet-mode.rules /etc/udev/rules.d/`
`sudo udevadm control --reload-rules`

3. Run the script:
`python3 tablet-mode.py`

## Auto-start

- Add to your desktop environment's Startup Applications.

## Future Plans

- [ ] Auto-detect tablet mode via accelerometer / lid-switch triggers.
- [ ] Configurable screen profile toggles.
- Note: Initial Unit Tests (using unittest and mock) are included for core logic. Full hardware-integration test coverage is in progress.