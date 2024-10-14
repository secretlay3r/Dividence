import time
import mss
import numpy as np
import ctypes
import threading
import random

VK_XBUTTON4 = 0x05
enabled = False
target_colors = []
monitor_resolution = (1920, 1080)
aimbot_fov = 75
aim_region = "body"
aimbot_mode = "smooth"
aimbot_speed = 1

color_ranges = {
    "ORANGE": {'r': (75, 108), 'g': (140, 244), 'b': (244, 255)},
    "YELLOW": {'r': (78, 133), 'g': (237, 255), 'b': (237, 255)},
    "PURPLE": {'r': (144, 255), 'g': (60, 99), 'b': (194, 255)},
    "RED": {'r': (80, 135), 'g': (100, 130), 'b': (247, 255)},
    "GREEN": {'r': (30, 97), 'g': (240, 255), 'b': (30, 110)},
    "CYAN": {'r': (246, 255), 'g': (246, 255), 'b': (66, 100)},
}

def set_aim_region(region):
    global aim_region
    aim_region = region

def set_monitor_resolution(width, height):
    global monitor_resolution
    monitor_resolution = (width, height)

def set_target_colors(selected_colors):
    global target_colors
    target_colors = [color_ranges[color] for color in selected_colors]

def set_aimbot_mode(mode):
    global aimbot_mode
    aimbot_mode = mode

def set_aimbot_speed(speed):
    global aimbot_speed
    aimbot_speed = speed

def toggle_aimbot(enable):
    global enabled
    enabled = enable
    if enabled:
        threading.Thread(target=run_aimbot, daemon=True).start()

def run_aimbot():
    sct = mss.mss()
    highres_region = get_highres_region()
    while enabled:
        screenshot = np.array(sct.grab(highres_region))
        for color_range in target_colors:
            target_pos = detect_color_in_range(screenshot, color_range)
            if target_pos:
                aim_at_target(target_pos, highres_region)
        time.sleep(0.001)

def set_aimbot_fov(fov):
    global aimbot_fov
    aimbot_fov = fov

def get_highres_region():
    width, height = monitor_resolution
    region_size = aimbot_fov * 2
    return {
        "top": int(height // 2 - region_size // 2),
        "left": int(width // 2 - region_size // 2),
        "width": int(region_size),
        "height": int(region_size)
    }

def detect_color_in_range(screenshot, color_range):
    r_min, r_max = color_range['r']
    g_min, g_max = color_range['g']
    b_min, b_max = color_range['b']

    mask = (
        (screenshot[:, :, 0] >= r_min) & (screenshot[:, :, 0] <= r_max) &
        (screenshot[:, :, 1] >= g_min) & (screenshot[:, :, 1] <= g_max) &
        (screenshot[:, :, 2] >= b_min) & (screenshot[:, :, 2] <= b_max)
    )

    y, x = np.where(mask)
    if x.size and y.size:
        avg_x = int(np.mean(x))
        avg_y = int(np.mean(y))
        return avg_x, avg_y
    return None

def aim_at_target(target_pos, highres):
    highres_center_x = highres['width'] // 2
    
    if aim_region == "body":
        highres_center_y = highres['height'] // 1.85
    elif aim_region == "head":
        highres_center_y = highres['height'] // 1.7
    elif aim_region == "random":
        highres_center_y = highres['height'] // random.uniform(1.67, 1.9)

    target_x, target_y = target_pos
    distance_x = target_x - highres_center_x
    distance_y = target_y - highres_center_y

    smooth_move(distance_x, distance_y)

def smooth_move(dx, dy):
    distance = np.sqrt(dx ** 2 + dy ** 2)
    if distance == 0:
        return

    step_size = max(1, distance / 10) * aimbot_speed
    num_steps = int(distance / step_size) + 1
    step_dx, step_dy = dx / num_steps, dy / num_steps

    for _ in range(num_steps):
        ctypes.windll.user32.mouse_event(0x0001, int(step_dx), int(step_dy), 0, 0)
        time.sleep(0.01 / aimbot_speed)
