import pystray
from PIL import Image, ImageDraw
import subprocess
import threading
import pydbus
import time
import glob
import re


def get_device(device_name):
    for name_file in glob.glob("/sys/class/input/event*/device/name"):
        try:
            with open(name_file, 'r') as f:
                content = f.read().strip()
                if content == device_name:
                    parts = name_file.split('/')
                    event_dir = next(p for p in parts if p.startswith('event'))
                    return f"/sys/class/input/{event_dir}/device/inhibited"
        except:
            continue
    return None

KEYBOARD_INHIBIT = get_device("AT Translated Set 2 keyboard")
TOUCHPAD_INHIBIT = get_device("ELAN030D:00 04F3:3352 Touchpad")

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
        with open(KEYBOARD_INHIBIT, "w") as f:
            f.write("1")
        with open(TOUCHPAD_INHIBIT, "w") as f:
            f.write("1")
    else:
        with open(KEYBOARD_INHIBIT, "w") as f:
            f.write("0")
        with open(TOUCHPAD_INHIBIT, "w") as f:
            f.write("0")

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


def get_current_rotation():
    result = subprocess.run(["kscreen-doctor", "--outputs"], capture_output=True, text=True)
    dc = result.stdout
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    clean_dc = ansi_escape.sub('', dc)
    match = re.search(r"eDP-1\s+.*?Rotation:\s*(\d+)", clean_dc, re.DOTALL)
    if match:
        rotation_number = match.group(1)
    return rotation_number

def rotate_right():
    current = get_current_rotation()
    new = None
    match current:
        case "1":
            new = "right"
        case "8":
            new = "inverted"
        case "4":
            new = "left"
        case "2":
            new = "normal"

    subprocess.run(["kscreen-doctor", f"output.eDP-1.rotation.{new}"])

def rotate_left():
    current = get_current_rotation()
    new = None
    match current:
        case "1":
            new = "left"
        case "2":
            new = "inverted"
        case "4":
            new = "right"
        case "8":
            new = "normal"
    subprocess.run(["kscreen-doctor", f"output.eDP-1.rotation.{new}"])


menu = pystray.Menu(pystray.MenuItem("Toggle", on_toggle), pystray.MenuItem("Quit", icon_quit), pystray.MenuItem("Rotate right", rotate_right), pystray.MenuItem("Rotate left", rotate_left))
icon = pystray.Icon("tablet_toggle", draw(), "Toggle Keyboard/Touchpad", menu)
icon.run()