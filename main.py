import keyboard
import triggerbot
import norecoil
import aimbot
import autoswap
import bhop
import winsound
import dearpygui.dearpygui as dpg
import json
import ctypes

aimbot_speed = 0.9
scan_area_size = 20
selected_resolution = "1920x1080"
x_recoil_compensation = 2.0
y_recoil_compensation = 2.0

aimbot_toggle_keys = ["F1"]
triggerbot_toggle_keys = ["F2"]

aimbot_toggled = False
triggerbot_toggled = False

aimbot_on_hold = False
triggerbot_on_hold = False
aimbot_hold_key = "Mouse 2"
triggerbot_hold_key = "Mouse 2"

aim_region = "body"

keys = {
    'a': "A", 'b': "B", 'c': "C", 'd': "D", 'e': "E", 'f': "F", 'g': "G", 'h': "H", 'i': "I", 'j': "J", 'k': "K", 'l': "L", 'm': "M", 'n': "N", 'o': "O", 'p': "P", 'q': "Q", 'r': "R", 's': "S", 't': "T", 'u': "U", 'v': "V", 'w': "W", 'x': "X", 'y': "Y", 'z': "Z",
    '0': "0", '1': "1", '2': "2", '3': "3", '4': "4", '5': "5", '6': "6", '7': "7", '8': "8", '9': "9",
    'space': "SPACE", 'enter': "ENTER", 'backspace': "BACKSPACE", 'tab': "TAB", 'capslock': "CAPSLOCK",
    'esc': "ESC", 'minus': "-", 'equals': "=", 'leftbracket': "[", 'rightbracket': "]", 'backslash': "\\",
    'semicolon': ";", 'apostrophe': "'", 'comma': ",", 'period': ".", 'forwardslash': "/", 'f4': "F4", 'f5': "F5",
    'f6': "F6", 'f7': "F7", 'f8': "F8", 'f9': "F9", 'f10': "F10", 'f11': "F11", 'f12': "F12", 'uparrow': "UP ARROW",
    'downarrow': "DOWN ARROW", 'leftarrow': "LEFT ARROW", 'rightarrow': "RIGHT ARROW", 'home': "HOME", 'end': "END",
    'pageup': "PAGE UP", 'pagedown': "PAGE DOWN", 'windows': "WINDOWS KEY", 'command': "COMMAND", 'option': "OPTION",
    'fn': "FUNCTION", 'insert': "INSERT", 'delete': "DELETE", 'pausebreak': "PAUSE/BREAK", 'scrolllock': "SCROLL LOCK",
    'numlock': "NUM LOCK"
}

def save_config(filename="config.json"):
    config = {
        "resolution_combo": dpg.get_value("resolution_combo"),
        "aimbot_speed_slider": dpg.get_value("aimbot_speed_slider"),
        "aimbot_on_hold": dpg.get_value("aimbot_on_hold"),
        "aimbot_hold_key_field": dpg.get_value("aimbot_hold_key_field"),
        "aimbot_key_field": dpg.get_value("aimbot_key_field"),
        "triggerbot_on_hold": dpg.get_value("triggerbot_on_hold"),
        "triggerbot_hold_key_field": dpg.get_value("triggerbot_hold_key_field"),
        "triggerbot_key_field": dpg.get_value("triggerbot_key_field"),
        "scan_area_slider": dpg.get_value("scan_area_slider"),
        "x_recoil_slider": dpg.get_value("x_recoil_slider"),
        "y_recoil_slider": dpg.get_value("y_recoil_slider"),
        "autoswap_checkbox": dpg.get_value("autoswap_checkbox"),
        "bhop_checkbox": dpg.get_value("bhop_checkbox")
    }
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)

def load_config(filename="config.json"):
    try:
        with open(filename, "r") as f:
            config = json.load(f)
            
            required_keys = [
                "resolution_combo", "aimbot_speed_slider", "aimbot_on_hold",
                "aimbot_hold_key_field", "aimbot_key_field", "triggerbot_on_hold",
                "triggerbot_hold_key_field", "triggerbot_key_field", "scan_area_slider",
                "x_recoil_slider", "y_recoil_slider", "autoswap_checkbox", "bhop_checkbox"
            ]
                        
            for key, value in config.items():
                if dpg.does_item_exist(key):
                    try:
                        if isinstance(value, bool):
                            dpg.set_value(key, value)
                        elif isinstance(value, str):
                            if key.endswith("_combo") or key.endswith("_field"):
                                dpg.set_value(key, value)
                        elif isinstance(value, float):
                            if key.endswith("_slider"):
                                dpg.set_value(key, value)
                    except Exception as e:
                        pass
                else:
                    pass
            
            if "color_set_combo" in config:
                set_color_range(config["color_set_combo"])
            
            dpg.set_value("aimbot_checkbox", dpg.get_value("aimbot_on_hold"))
            dpg.set_value("triggerbot_checkbox", dpg.get_value("triggerbot_on_hold"))
            
    except FileNotFoundError:
        print("Config.json does not exist!")
        
def set_color_range(selected_color):
    triggerbot.set_target_colors([selected_color])
    aimbot.set_target_colors([selected_color])

def set_resolution(sender, app_data):
    global selected_resolution
    selected_resolution = app_data
    if selected_resolution == "1920x1080":
        aimbot.set_monitor_resolution(1920, 1080)
        triggerbot.set_monitor_resolution(1920, 1080)
        autoswap.set_monitor_resolution(1920, 1080)
    else:
        aimbot.set_monitor_resolution(1280, 720)
        triggerbot.set_monitor_resolution(1280, 720)
        autoswap.set_monitor_resolution(1280, 720)

def toggle_autoswap(sender, app_data):
    if dpg.get_value(sender):
        autoswap.toggle_autoswap(True)
        winsound.Beep(1000, 200)
    else:
        autoswap.toggle_autoswap(False)
        winsound.Beep(500, 200)

def toggle_aimbot(sender, app_data):
    if dpg.get_value(sender):
        aimbot.toggle_aimbot(enable=True)
        winsound.Beep(1000, 200)
    else:
        aimbot.toggle_aimbot(enable=False)
        winsound.Beep(500, 200)

def set_aim_region(sender, app_data):
    global aim_region
    aim_region = app_data
    aimbot.set_aim_region(aim_region)

def set_aimbot_speed(sender, app_data=None):
    global aimbot_speed
    aimbot_speed = dpg.get_value(sender)
    aimbot.set_aimbot_speed(aimbot_speed)

def toggle_triggerbot(sender, app_data):
    if dpg.get_value(sender):
        triggerbot.toggle_triggerbot(enable=True)
        winsound.Beep(1000, 200)
    else:
        triggerbot.toggle_triggerbot(enable=False)
        winsound.Beep(500, 200)

def set_scan_area(sender, app_data):
    global scan_area_size
    scan_area_size = dpg.get_value(sender)
    triggerbot.set_scan_area_size(scan_area_size)

def toggle_norecoil(sender, app_data):
    norecoil.toggle_norecoil()

def set_x_recoil(sender, app_data):
    global x_recoil_compensation
    x_recoil_compensation = dpg.get_value(sender)
    norecoil.horizontal_range = x_recoil_compensation

def set_y_recoil(sender, app_data):
    global y_recoil_compensation
    y_recoil_compensation = dpg.get_value(sender)
    norecoil.vertical_range = y_recoil_compensation

def assign_key(field):
    key = keyboard.read_event()
    if key.event_type == keyboard.KEY_DOWN:
        assigned_key = keys.get(key.name.lower(), key.name.upper())
        if field == "aimbot":
            global aimbot_toggle_keys
            aimbot_toggle_keys = [assigned_key]
            dpg.set_value("aimbot_key_field", assigned_key)
        elif field == "triggerbot":
            global triggerbot_toggle_keys
            triggerbot_toggle_keys = [assigned_key]
            dpg.set_value("triggerbot_key_field", assigned_key)
        elif field == "aimbot_hold":
            global aimbot_hold_key
            aimbot_hold_key = assigned_key
            dpg.set_value("aimbot_hold_key_field", assigned_key)
        elif field == "triggerbot_hold":
            global triggerbot_hold_key
            triggerbot_hold_key = assigned_key
            dpg.set_value("triggerbot_hold_key_field", assigned_key)

def reset_hold_key(field):
    global aimbot_hold_key, triggerbot_hold_key
    if field == "aimbot_hold":
        aimbot_hold_key = "Mouse 2"
        dpg.set_value("aimbot_hold_key_field", "Mouse 2")
    elif field == "triggerbot_hold":
        triggerbot_hold_key = "Mouse 2"
        dpg.set_value("triggerbot_hold_key_field", "Mouse 2")

def is_right_mouse_button_down():
    return ctypes.windll.user32.GetAsyncKeyState(0x02) != 0

def is_key_held(key):
    if key.lower() == "mouse 2":
        return ctypes.windll.user32.GetAsyncKeyState(0x02) != 0
    else:
        return keyboard.is_pressed(key.lower())

def check_toggle_keys():
    global aimbot_toggled, triggerbot_toggled
    global aimbot_on_hold, triggerbot_on_hold

    if keyboard.is_pressed(aimbot_toggle_keys[0]):
        if not aimbot_on_hold:
            aimbot_toggled = not aimbot_toggled
            dpg.set_value("aimbot_checkbox", aimbot_toggled)
            aimbot.toggle_aimbot(aimbot_toggled)
            winsound.Beep(1000 if aimbot_toggled else 500, 200)
            aimbot_on_hold = True
    else:
        aimbot_on_hold = False

    if keyboard.is_pressed(triggerbot_toggle_keys[0]):
        if not triggerbot_on_hold:
            triggerbot_toggled = not triggerbot_toggled
            dpg.set_value("triggerbot_checkbox", triggerbot_toggled)
            triggerbot.toggle_triggerbot(triggerbot_toggled)
            winsound.Beep(1000 if triggerbot_toggled else 500, 200)
            triggerbot_on_hold = True
    else:
        triggerbot_on_hold = False 

    if is_key_held(aimbot_hold_key):
        if dpg.get_value("aimbot_on_hold") and not dpg.get_value("aimbot_checkbox"):
            dpg.set_value("aimbot_checkbox", True)
            aimbot.toggle_aimbot(True)
    else:
        if dpg.get_value("aimbot_on_hold") and dpg.get_value("aimbot_checkbox"):
            dpg.set_value("aimbot_checkbox", False)
            aimbot.toggle_aimbot(False)

    if is_key_held(triggerbot_hold_key):
        if dpg.get_value("triggerbot_on_hold") and not dpg.get_value("triggerbot_checkbox"):
            dpg.set_value("triggerbot_checkbox", True)
            triggerbot.toggle_triggerbot(True)
    else:
        if dpg.get_value("triggerbot_on_hold") and dpg.get_value("triggerbot_checkbox"):
            dpg.set_value("triggerbot_checkbox", False)
            triggerbot.toggle_triggerbot(False)

def apply_custom_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvCheckbox):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (133, 127, 155))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 50))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 70, 70))
        with dpg.theme_component(dpg.mvSliderFloat):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (133, 127, 155))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (133, 127, 155))
    dpg.bind_theme(theme)

dpg.create_context()

apply_custom_theme()

with dpg.window(tag="primary_window"):
    dpg.set_primary_window("primary_window", True)

    with dpg.tab_bar():
        with dpg.tab(label="Config"):
            dpg.add_combo(label="Monitor Resolution", items=["1280x720", "1920x1080"], callback=set_resolution, tag="resolution_combo")
            dpg.add_combo(label="Color Set", items=["ORANGE", "YELLOW", "PURPLE", "RED", "GREEN", "CYAN"], callback=lambda sender, app_data: set_color_range(app_data))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save Config", callback=lambda: save_config())
                dpg.add_button(label="Load Config", callback=lambda: load_config())

        with dpg.tab(label="Aimbot"):
            dpg.add_checkbox(label="Aimbot", callback=toggle_aimbot, tag="aimbot_checkbox")
            dpg.add_combo(label="Aim Region", items=["body", "head", "hitscan"], callback=set_aim_region, tag="aim_region_combo")
            dpg.add_slider_float(label="Aimbot Speed", default_value=0.9, min_value=0.1, max_value=2.0, callback=set_aimbot_speed, tag="aimbot_speed_slider")
            dpg.add_checkbox(label="Hold-to-use", callback=lambda sender, app_data: dpg.set_value("aimbot_on_hold", app_data), tag="aimbot_on_hold")
            dpg.add_input_text(label="Hold Key", default_value="Mouse 2", readonly=True, tag="aimbot_hold_key_field")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Set Hold Key", callback=lambda: assign_key("aimbot_hold"))
                dpg.add_button(label="Reset Hold Key", callback=lambda: reset_hold_key("aimbot_hold"))
            dpg.add_input_text(label="Toggle Key", default_value="F1", readonly=True, tag="aimbot_key_field")
            dpg.add_button(label="Set Toggle Key", callback=lambda: assign_key("aimbot"))

        with dpg.tab(label="Triggerbot"):
            dpg.add_checkbox(label="Triggerbot", callback=toggle_triggerbot, tag="triggerbot_checkbox")
            dpg.add_slider_float(label="Scan Area", default_value=15, min_value=10, max_value=200, callback=set_scan_area, tag="scan_area_slider")
            dpg.add_checkbox(label="Hold-to-use", callback=lambda sender, app_data: dpg.set_value("triggerbot_on_hold", app_data), tag="triggerbot_on_hold")
            dpg.add_input_text(label="Hold Key", default_value="Mouse 2", readonly=True, tag="triggerbot_hold_key_field")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Set Hold Key", callback=lambda: assign_key("triggerbot_hold"))
                dpg.add_button(label="Reset Hold Key", callback=lambda: reset_hold_key("triggerbot_hold"))
            dpg.add_input_text(label="Toggle Key", default_value="F2", readonly=True, tag="triggerbot_key_field")
            dpg.add_button(label="Set Toggle Key", callback=lambda: assign_key("triggerbot"))

        with dpg.tab(label="NoRecoil"):
            dpg.add_checkbox(label="Recoil Compensation", callback=toggle_norecoil)
            dpg.add_slider_float(label="X-Axis Recoil", default_value=2.0, min_value=0, max_value=10, callback=set_x_recoil, tag="x_recoil_slider")
            dpg.add_slider_float(label="Y-Axis Recoil", default_value=2.0, min_value=0, max_value=10, callback=set_y_recoil, tag="y_recoil_slider")

        with dpg.tab(label="Misc"):
            dpg.add_checkbox(label="Auto swap to spectre", callback=toggle_autoswap, tag="autoswap_checkbox")
            dpg.add_checkbox(label="Bunny Hop", callback=lambda sender, app_data: bhop.toggle_bhop(app_data), tag="bhop_checkbox")

dpg.create_viewport(title='Dividence', width=510, height=370)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    check_toggle_keys()
    dpg.render_dearpygui_frame()

dpg.destroy_context()
