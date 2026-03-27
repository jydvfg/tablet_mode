import pystray
from PIL import Image, ImageDraw
import subprocess
import os

KEYBOARD_INHIBIT = "/sys/class/input/event3/device/inhibited"
TOUCHPAD_INHIBIT = "/sys/class/input/event5/device/inhibited"

def check_state():
    k_state = 0
    t_state = 0
    with open(KEYBOARD_INHIBIT, 'r') as f:
        k_state = f.read().strip()
    with open(TOUCHPAD_INHIBIT, 'r') as f:
        t_state = f.read().strip()
    
    
    if k_state == "0" and t_state == "0":
        return True
    elif k_state == "1" and t_state == "1":
        return False
    else:
        print("invalid values")
        return

def toggle():
    current_state = check_state()
    if current_state:
        subprocess.run(["sudo", "tee", KEYBOARD_INHIBIT], input="1", text=True, check=True)
        subprocess.run(["sudo", "tee", TOUCHPAD_INHIBIT], input="1", text=True, check=True)
    else:
        subprocess.run(["sudo", "tee", KEYBOARD_INHIBIT], input="0", text=True, check=True)
        subprocess.run(["sudo", "tee", TOUCHPAD_INHIBIT], input="0", text=True, check=True)

def draw():
    current_state = check_state()

    if current_state:
        image = Image.new('RGBA', (64,64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 63, 63), fill=(0, 255, 0, 255))

        return image
    else:
        image = Image.new('RGBA', (64,64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 63, 63), fill=(255, 0, 0, 255))

        return image

def on_toggle(icon, item):
    toggle()
    icon.icon = draw()

def icon_quit(icon, item):
    icon.stop()

menu = pystray.Menu(pystray.MenuItem("Toggle", on_toggle), pystray.MenuItem("Quit", icon_quit))
icon = pystray.Icon("tablet_toggle", draw(), "Toggle Keyboard/Touchpad", menu)

icon.run()