import pystray
from PIL import Image, ImageDraw
import subprocess
import threading
import pydbus
import time


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


def get_current_rotation():
    bus = pydbus.SessionBus()
    dc = bus.get('org.gnome.Mutter.DisplayConfig', '/org/gnome/Mutter/DisplayConfig')
    state = dc.GetCurrentState()
    for cfg in state[2]:
        for out in cfg[5]:
            if out[0] == 'eDP-1':
                return ['normal', 'right', 'inverted', 'left'][cfg[3]]
    return 'normal'

def rotate_right():
    current = get_current_rotation()
    new = None
    match current:
        case "normal":
            new = "right"
        case "right":
            new = "inverted"
        case "inverted":
            new = "left"
        case "left":
            new = "normal"

    subprocess.run(["/home/juan-yuste-del-valle/.cargo/bin/gnome-randr", "modify", "eDP-1", "--rotate", new])

def rotate_left():
    current = get_current_rotation()
    new = None
    match current:
        case "normal":
            new = "left"
        case "left":
            new = "inverted"
        case "inverted":
            new = "right"
        case "right":
            new = "normal"
    subprocess.run(["/home/juan-yuste-del-valle/.cargo/bin/gnome-randr", "modify", "eDP-1", "--rotate", new])


menu = pystray.Menu(pystray.MenuItem("Toggle", on_toggle), pystray.MenuItem("Quit", icon_quit), pystray.MenuItem("Rotate right", rotate_right), pystray.MenuItem("Rotate left", rotate_left))
icon = pystray.Icon("tablet_toggle", draw(), "Toggle Keyboard/Touchpad", menu)
if __name__ == "__main__":
    icon.run()