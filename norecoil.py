import time
import win32api
import random
import ctypes
import threading

horizontal_range = 2.0
vertical_range = 2.0
downward_range = 4.0
compensation_interval = 0.03
enabled = False

chance = 0.1
x_rand_move = 3.2

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
    if random.random() < chance:
        horizontal_offset = random.uniform(-x_rand_move, x_rand_move)
    else:
        horizontal_offset = random.uniform(-horizontal_range, horizontal_range)

    vertical_offset = random.uniform(-vertical_range, vertical_range) + downward_range
    ctypes.windll.user32.mouse_event(0x0001, int(horizontal_offset), int(vertical_offset), 0, 0)

def set_compensation_speed(new_interval):
    global compensation_interval
    compensation_interval = new_interval

def set_compensation_interval(new_interval):
    global compensation_interval
    compensation_interval = new_interval
    
def set_x_recoil(new_horizontal_range):
    global horizontal_range
    horizontal_range = new_horizontal_range

def set_y_recoil(new_vertical_range):
    global vertical_range
    vertical_range = new_vertical_range

def set_chance(upd_chance):
    global chance
    chance = upd_chance

def set_x_rand_move(new_x_rand_move):
    global x_rand_move
    x_rand_move = new_x_rand_move
