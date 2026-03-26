# Tablet Mode Toggle

System tray utility for 2-in-1 laptops to disable keyboard and touchpad in tablet mode.

## Current Features

- System tray icon (green = enabled, red = disabled)
- One-click toggle to disable/enable both keyboard and touchpad
- Works on Wayland
- Uses sysfs inhibition (no X11 dependencies)

## Requirements

- Python 3
- `pystray` and `python3-pil`
- udev (for permission persistence)

## Installation

1. Install dependencies:
