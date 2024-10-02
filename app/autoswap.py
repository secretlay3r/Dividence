import time
import pyautogui
import mss
import numpy as np
import threading
import keyboard
import cv2

enabled = False
monitor_resolution = (1920, 1080)
top_monitor_height = 100
scan_area_width = int(monitor_resolution[0] * 0.5)

target_color_range = {
    "r": (60, 75),
    "g": (205, 215),
    "b": (237, 255)
}

def set_monitor_resolution(width, height):
    global monitor_resolution, scan_area_width
    monitor_resolution = (width, height)
    scan_area_width = width

def toggle_autoswap(enable):
    global enabled
    enabled = enable
    if enabled:
        threading.Thread(target=run_autoswap, daemon=True).start()

def run_autoswap():
    sct = mss.mss()
    monitor = {
        "top": 160,
        "left": 0,
        "width": scan_area_width,
        "height": top_monitor_height
    }

    consistent_detection_count = 0
    detection_threshold = 1

    while enabled:
        screenshot = np.array(sct.grab(monitor))
        
        if screenshot.size == 0:
            continue

        screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        if detect_target_color(screenshot):
            consistent_detection_count += 1
        else:
            consistent_detection_count = 0

        if consistent_detection_count >= detection_threshold:
            press_x()
            consistent_detection_count = 0

        time.sleep(0.01)

    cv2.destroyAllWindows()

def detect_target_color(screenshot):
    r_min, r_max = target_color_range["r"]
    g_min, g_max = target_color_range["g"]
    b_min, b_max = target_color_range["b"]

    mask = (
        (screenshot[:, :, 0] >= r_min) & (screenshot[:, :, 0] <= r_max) &
        (screenshot[:, :, 1] >= g_min) & (screenshot[:, :, 1] <= g_max) &
        (screenshot[:, :, 2] >= b_min) & (screenshot[:, :, 2] <= b_max)
    )
    
    return np.any(mask)

def press_x():
    keyboard.press_and_release('x')
    time.sleep(4)
