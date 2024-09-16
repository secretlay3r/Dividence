import time
import mss
import numpy as np
import ctypes
import threading

VK_XBUTTON4 = 0x05
enabled = False
target_colors = []
aimbot_speed = 0.9
monitor_resolution = (1920, 1080)  # Default resolution

# Color ranges for detection
color_ranges = {
    "ORANGE": {'r': (75, 108), 'g': (140, 244), 'b': (244, 255)},
    "YELLOW": {'r': (78, 133), 'g': (237, 255), 'b': (237, 255)},
    "PURPLE": {'r': (144, 255), 'g': (60, 99), 'b': (194, 255)},
    "RED": {'r': (80, 135), 'g': (100, 130), 'b': (247, 255)},
    "GREEN": {'r': (30, 97), 'g': (240, 255), 'b': (30, 110)},
    "CYAN": {'r': (246, 255), 'g': (246, 255), 'b': (66, 100)},
}

def set_monitor_resolution(width, height):
    global monitor_resolution
    monitor_resolution = (width, height)

def set_target_colors(selected_colors):
    global target_colors
    target_colors = [color_ranges[color] for color in selected_colors]

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

def get_highres_region():
    width, height = monitor_resolution
    return {"top": height // 2 - 200, "left": width // 2 - 200, "width": 400, "height": 400}

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
    highres_center_y = highres['height'] // 2

    target_x, target_y = target_pos
    distance_x = target_x - highres_center_x
    distance_y = target_y - highres_center_y

    if abs(distance_x) > 2 or abs(distance_y) > 2:
        smooth_move(distance_x, distance_y)

def smooth_move(dx, dy, speed_factor=None):
    speed_factor = speed_factor or aimbot_speed
    distance = np.sqrt(dx ** 2 + dy ** 2)
    if distance == 0:
        return

    step_size = max(1, distance / 10) * speed_factor
    num_steps = int(distance / step_size) + 1
    step_dx, step_dy = dx / num_steps, dy / num_steps

    for _ in range(num_steps):
        ctypes.windll.user32.mouse_event(0x0001, int(step_dx), int(step_dy), 0, 0)
        time.sleep(0.01 / speed_factor)
