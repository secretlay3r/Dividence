import time
import win32api
import random
import ctypes
import threading

horizontal_range = 2
vertical_range = 2
downward_range = 4
compensation_interval = 0.03
enabled = False

def is_mouse_down():
    lmb_state = win32api.GetKeyState(0x01)
    return lmb_state < 0

def toggle_norecoil():
    global enabled
    enabled = not enabled
    if enabled:
        threading.Thread(target=start_norecoil_loop, daemon=True).start()

def start_norecoil_loop():
    while enabled:
        if is_mouse_down():
            while is_mouse_down():
                apply_recoil_compensation()
                time.sleep(compensation_interval)
            time.sleep(0.001)
        else:
            time.sleep(0.01)

def apply_recoil_compensation():
    horizontal_offset = random.uniform(-horizontal_range, horizontal_range)
    vertical_offset = random.uniform(-vertical_range, vertical_range) + downward_range

    ctypes.windll.user32.mouse_event(0x0001, int(horizontal_offset), int(vertical_offset), 0, 0)
