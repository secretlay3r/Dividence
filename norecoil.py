import time
import win32api
import random
import ctypes
import threading

horizontal_range = 2
vertical_range = 2
downward_range = 4
min_firerate = 0.04
max_firerate = 0.05
compensation_interval = 0.03

enabled = False

def is_mouse_down():
    lmb_state = win32api.GetKeyState(0x01)
    return lmb_state < 0

def toggle_norecoil():
    global enabled
    enabled = not enabled
    if enabled:
        start_norecoil_loop()

def start_norecoil_loop():
    def loop():
        global enabled
        while True:
            if is_mouse_down() and enabled:
                while is_mouse_down():
                    offset_const = 1000
                    
                    horizontal_offset = random.uniform(-horizontal_range * offset_const, horizontal_range * offset_const) / offset_const
                    vertical_offset = random.uniform(-vertical_range * offset_const, vertical_range * offset_const) / offset_const
                    downward_offset = random.uniform(3, downward_range * offset_const) / offset_const

                    ctypes.windll.user32.mouse_event(0x1, int(horizontal_offset), int(vertical_offset + downward_offset), 0, 0)
                    time.sleep(compensation_interval)
                
                time.sleep(0.001)
            else:
                time.sleep(0.01)

    threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    start_norecoil_loop()
