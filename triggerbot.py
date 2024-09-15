import time
import pyautogui
import mss
import numpy as np
import ctypes
import threading
import random

pyautogui.FAILSAFE = False

VK_XBUTTON4 = 0x05

enabled = False
target_colors = []
scan_area_size = 20
monitor_resolution = (1920, 1080)  # Default res

color_ranges = {
    "ORANGE": {'r': (75, 108), 'g': (140, 244), 'b': (244, 255)},  # #C57824
    "YELLOW": {'r': (78, 133), 'g': (237,255), 'b': (237,255)},  # #FFFF3D
    "PURPLE": {'r': (144, 255), 'g': (60, 99), 'b': (194, 255)},  # #FF33FF
    "RED": {'r': (80, 135), 'g': (100, 130), 'b': (247, 255)},  # #FF3132
    "GREEN": {'r': (30, 97), 'g': (240, 255), 'b': (30, 110)},  # #2EFB00
    "CYAN": {'r': (246, 255), 'g': (246, 255), 'b': (66, 100)},  # #00FFFF
}

def set_monitor_resolution(width, height):
    global monitor_resolution
    monitor_resolution = (width, height)

def set_target_colors(selected_colors):
    global target_colors
    target_colors = [color_ranges[color] for color in selected_colors]

def toggle_triggerbot(enable):
    global enabled
    enabled = enable
    if enabled:
        threading.Thread(target=run_triggerbot, daemon=True).start()

def set_scan_area_size(new_size):
    global scan_area_size
    scan_area_size = int(new_size)

def run_triggerbot():
    sct = mss.mss()
    lower_delay, upper_delay = 0.005, 0.02  # Randomized delay range between shots
    monitor = get_monitor_region()

    while enabled:
        screenshot = np.array(sct.grab(monitor))
        for color_range in target_colors:
            if detect_color_in_range(screenshot, color_range):
                shoot()
                time.sleep(random.uniform(lower_delay, upper_delay))  # Random delay between clicks
        time.sleep(0.001)

def get_monitor_region():
    if monitor_resolution == (1920, 1080):
        monitor = {
            "top": 540 - scan_area_size // 2,
            "left": 960 - scan_area_size // 2,
            "width": scan_area_size,
            "height": scan_area_size
        }
    elif monitor_resolution == (1280, 720):
        monitor = {
            "top": int(540 * 720 / 1080) - scan_area_size // 2,
            "left": int(960 * 1280 / 1920) - scan_area_size // 2,
            "width": int(scan_area_size * 1280 / 1920),
            "height": int(scan_area_size * 720 / 1080)
        }
    else:
        raise ValueError("Unsupported resolution")
    return monitor

def detect_color_in_range(screenshot, color_range):
    r_min, r_max = color_range['r']
    g_min, g_max = color_range['g']
    b_min, b_max = color_range['b']

    mask = (
        (screenshot[:, :, 0] >= r_min) & (screenshot[:, :, 0] <= r_max) &
        (screenshot[:, :, 1] >= g_min) & (screenshot[:, :, 1] <= g_max) &
        (screenshot[:, :, 2] >= b_min) & (screenshot[:, :, 2] <= b_max)
    )

    return np.any(mask)

def shoot():
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # Left button down
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # Left button up

def get_key_state(key_code):
    return ctypes.windll.user32.GetAsyncKeyState(key_code)

def main():
    global enabled
    frame_rate = 900
    interval = 1.0 / frame_rate

    while True:
        if get_key_state(VK_XBUTTON4) & 0x8000:
            if not enabled:
                toggle_triggerbot(True)
            time.sleep(0.1)  # Prevent rapid toggling
        elif not (get_key_state(VK_XBUTTON4) & 0x8000) and enabled:
            toggle_triggerbot(False)
        time.sleep(interval)

if __name__ == "__main__":
    main()
