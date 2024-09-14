import time
import mss
import numpy as np
import ctypes
import threading

VK_XBUTTON4 = 0x05
enabled = False
target_colors = []
aimbot_speed = 0.9

color_ranges = {
    "ORANGE": {'r': (75, 108), 'g': (140, 244), 'b': (244, 255)},  # #C57824
    "YELLOW": {'r': (78, 133), 'g': (237,255), 'b': (237,255)},  # #FFFF3D
    "PURPLE": {'r': (144, 255), 'g': (60, 99), 'b': (194, 255)},  # #FF33FF
    "RED": {'r': (80, 135), 'g': (100, 130), 'b': (247, 255)},  # #FF3132
    "GREEN": {'r': (30, 97), 'g': (240, 255), 'b': (30, 110)},  # #2EFB00
    "CYAN": {'r': (246, 255), 'g': (246, 255), 'b': (66, 100)},  # #00FFFF
}

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
    monitor = {"top": 400, "left": 760, "width": 400, "height": 400}  # FOV

    while enabled:
        screenshot = np.array(sct.grab(monitor))
        for color_range in target_colors:
            target_pos = detect_color_in_range(screenshot, color_range)
            if target_pos:
                aim_at_target(target_pos, monitor)
        time.sleep(0.001)

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
    if len(x) == 0 or len(y) == 0:
        return None

    avg_x = int(np.mean(x))
    avg_y = int(np.mean(y))

    return (avg_x, avg_y)

def aim_at_target(target_pos, monitor):
    monitor_center_x = monitor['width'] // 2
    monitor_center_y = monitor['height'] // 2

    target_x, target_y = target_pos

    distance_x = target_x - monitor_center_x
    distance_y = target_y - monitor_center_y

    offset_x = 0
    offset_y = 53

    distance_x += offset_x
    distance_y += offset_y

    if abs(distance_x) > 2 or abs(distance_y) > 2:  # Deadzone
        smooth_move(distance_x, distance_y)

def smooth_move(dx, dy, speed_factor=None):
    if speed_factor is None:
        speed_factor = aimbot_speed

    distance = np.sqrt(dx**2 + dy**2)
    if distance == 0:
        return

    step_size = max(1, distance / 10) * speed_factor
    num_steps = int(distance / step_size) + 1
    step_dx, step_dy = dx / num_steps, dy / num_steps

    for _ in range(num_steps):
        ctypes.windll.user32.mouse_event(0x0001, int(step_dx), int(step_dy), 0, 0)
        time.sleep(0.01 / speed_factor)

def get_key_state(key_code):
    return ctypes.windll.user32.GetAsyncKeyState(key_code)

def main():
    global enabled
    frame_rate = 900
    interval = 1.0 / frame_rate

    while True:
        if get_key_state(VK_XBUTTON4) & 0x8000:
            if not enabled:
                toggle_aimbot(True)
            time.sleep(0.1)  # Prevent rapid toggling
        elif not (get_key_state(VK_XBUTTON4) & 0x8000) and enabled:
            toggle_aimbot(False)
        time.sleep(interval)

if __name__ == "__main__":
    main()