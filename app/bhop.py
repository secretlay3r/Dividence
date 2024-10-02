import keyboard
import threading
import time

bhop_enabled = False

def toggle_bhop(enable):
    global bhop_enabled
    bhop_enabled = enable
    if bhop_enabled:
        threading.Thread(target=bhop_loop, daemon=True).start()

def bhop_loop():
    while bhop_enabled:
        if keyboard.is_pressed('space'):
            while keyboard.is_pressed('space'):
                keyboard.press('space')
                time.sleep(0.02)
                keyboard.release('space')
                time.sleep(0.02)
        time.sleep(0.01)