import time
import win32api
import random
import ctypes
import threading

horizontal_range = 2
vertical_range = 3
downward_range = 14
min_firerate = 0.04
max_firerate = 0.05

enabled = False

def is_mouse_down():
    """ Check if the left mouse button is pressed. """
    lmb_state = win32api.GetKeyState(0x01)
    return lmb_state < 0

def toggle_norecoil():
    """ Toggle the no-recoil feature. """
    global enabled
    enabled = not enabled
    if enabled:
        start_norecoil_loop()

def start_norecoil_loop():
    """ Start the no-recoil loop in a separate thread. """
    def loop():
        global enabled
        while True:
            if is_mouse_down() and enabled:
                offset_const = 1000
                
                horizontal_offset = random.uniform(-horizontal_range * offset_const, horizontal_range * offset_const) / offset_const
                vertical_offset = random.uniform(-vertical_range * offset_const, vertical_range * offset_const) / offset_const
                downward_offset = random.uniform(3, downward_range * offset_const) / offset_const

                # Move the mouse to compensate for recoil
                ctypes.windll.user32.mouse_event(0x1, int(horizontal_offset), int(vertical_offset + downward_offset), 0, 0)

                # Wait for a random amount of time between shots
                time_offset = random.uniform(min_firerate * offset_const, max_firerate * offset_const) / offset_const
                time.sleep(time_offset)
            
            time.sleep(0.001)

    threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    start_norecoil_loop()