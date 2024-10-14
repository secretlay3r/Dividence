import ctypes
import json
import os
import winsound
from pynput import keyboard as pynput_keyboard
from pynput import mouse as pynput_mouse
import dearpygui.dearpygui as dpg

import triggerbot
import norecoil
import aimbot
import autoswap
import bhop

from overlay import OverlayWindow
from utils import *

aimbot_fov = 75
aimbot_speed = 0.9
aim_region = "body"
aimbot_toggle_keys = ["F1"]
aimbot_hold_key = "Mouse 2"
aimbot_toggled = False
aimbot_on_hold = False

scan_area_size = 20
triggerbot_toggle_keys = ["F2"]
triggerbot_hold_key = "Mouse 2"
triggerbot_toggled = False
triggerbot_on_hold = False

x_recoil_compensation = 2.0
y_recoil_compensation = 2.0
compensation_interval = 0.065
norecoil_toggle_keys = ["F3"]
norecoil_hold_key = "Mouse 2"
norecoil_toggled = False
norecoil_on_hold = False

selected_resolution = "1920x1080"

overlay = OverlayWindow()

key_to_vk = {
    'MOUSE 1': 0x01,
    'MOUSE 2': 0x02,
    'MOUSE 3': 0x04,
    'MOUSE 4': 0x05,
    'MOUSE 5': 0x06,

    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,

    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
    'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
    'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
    'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
    'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
    'Z': 0x5A,

    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74,
    'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79,
    'F11': 0x7A, 'F12': 0x7B,

    'ENTER': 0x0D, 'ESC': 0x1B, 'SPACE': 0x20, 'LEFT SHIFT': 0xA0,
    'RIGHT SHIFT': 0xA1, 'LEFT CTRL': 0xA2, 'RIGHT CTRL': 0xA3,
    'LEFT ALT': 0xA4, 'RIGHT ALT': 0xA5,
}

def save_config(filename="config.json"):
    try:
        config = {
            "resolution_combo": dpg.get_value("resolution_combo"),
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
            "bhop_checkbox": dpg.get_value("bhop_checkbox"),
            "aim_region_combo": dpg.get_value("aim_region_combo"),
            "aimbot_fov_slider": dpg.get_value("aimbot_fov_slider"),
            "norecoil_on_hold": dpg.get_value("norecoil_on_hold"),
            "norecoil_hold_key_field": dpg.get_value("norecoil_hold_key_field"),
            "norecoil_key_field": dpg.get_value("norecoil_key_field"),
            "aimbot_fov_circle_visible": dpg.get_value("aimbot_fov_circle_checkbox"),
            "aimbot_fov_color": dpg.get_value("aimbot_fov_color_picker"),
            "triggerbot_fov_circle_visible": dpg.get_value("triggerbot_fov_circle_checkbox"),
            "triggerbot_fov_color": dpg.get_value("triggerbot_fov_color_picker"),
        }
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved to {filename}")
    except Exception as e:
        print(f"Error saving configuration: {e}")

def load_config(filename="config.json"):
    try:
        if not os.path.exists(filename):
            print(f"Config file does not exist. Creating new config.")
            return

        with open(filename, "r") as f:
            config = json.load(f)

        aimbot_color = config["aimbot_fov_color"]
        triggerbot_color = config["triggerbot_fov_color"]

        dpg.set_value("resolution_combo", config["resolution_combo"])
        dpg.set_value("aimbot_on_hold", config["aimbot_on_hold"])
        dpg.set_value("aimbot_hold_key_field", config["aimbot_hold_key_field"])
        dpg.set_value("aimbot_key_field", config["aimbot_key_field"])
        dpg.set_value("triggerbot_on_hold", config["triggerbot_on_hold"])
        dpg.set_value("triggerbot_hold_key_field", config["triggerbot_hold_key_field"])
        dpg.set_value("triggerbot_key_field", config["triggerbot_key_field"])
        dpg.set_value("scan_area_slider", config["scan_area_slider"])
        dpg.set_value("x_recoil_slider", config["x_recoil_slider"])
        dpg.set_value("y_recoil_slider", config["y_recoil_slider"])
        dpg.set_value("autoswap_checkbox", config["autoswap_checkbox"])
        dpg.set_value("bhop_checkbox", config["bhop_checkbox"])
        dpg.set_value("aim_region_combo", config["aim_region_combo"])
        dpg.set_value("aimbot_fov_slider", config["aimbot_fov_slider"])
        dpg.set_value("norecoil_on_hold", config["norecoil_on_hold"])
        dpg.set_value("norecoil_hold_key_field", config["norecoil_hold_key_field"])
        dpg.set_value("norecoil_key_field", config["norecoil_key_field"])

        dpg.configure_item("aimbot_fov_circle_checkbox", show=config["aimbot_fov_circle_visible"])
        dpg.configure_item("triggerbot_fov_circle_checkbox", show=config["triggerbot_fov_circle_visible"])

        dpg.set_value("aimbot_fov_color_picker", aimbot_color)
        dpg.set_value("triggerbot_fov_color_picker", triggerbot_color)

        set_aimbot_speed()
        set_aimbot_fov()
        set_scan_area()
        set_x_recoil()
        set_y_recoil()
        set_aim_region(None, dpg.get_value("aim_region_combo"))

        print(f"Your config.json loaded!")
    except FileNotFoundError:
        print(f"Looks like config.json does not exist!")

def set_color_range(selected_color):
    triggerbot.set_target_colors([selected_color])
    aimbot.set_target_colors([selected_color])


def set_resolution(sender, app_data):
    global selected_resolution
    selected_resolution = app_data
    width, height = map(int, selected_resolution.split('x'))
    aimbot.set_monitor_resolution(width, height)
    triggerbot.set_monitor_resolution(width, height)
    autoswap.set_monitor_resolution(width, height)

def toggle_autoswap(sender, app_data):
    enable = dpg.get_value(sender)
    autoswap.toggle_autoswap(enable)
    winsound.Beep(1000 if enable else 500, 200)

def toggle_aimbot(sender, app_data):
    enable = dpg.get_value(sender)
    aimbot.toggle_aimbot(enable)
    winsound.Beep(1000 if enable else 500, 200)

def set_aim_region(sender, app_data):
    global aim_region
    aim_region = app_data
    aimbot.set_aim_region(aim_region)

def set_aimbot_speed(sender=None, app_data=None):
    global aimbot_speed
    aimbot_speed = dpg.get_value(sender)
    aimbot.set_aimbot_speed(aimbot_speed)

def set_aimbot_mode(sender, app_data):
    global aimbot_smooth_mode
    aimbot_smooth_mode = app_data == "smooth"
    aimbot.set_aimbot_mode(aimbot_smooth_mode)
    
    if app_data == "custom":
        dpg.configure_item("aimbot_speed_slider", show=True)
        set_aimbot_speed()
    else:
        dpg.configure_item("aimbot_speed_slider", show=False)

    if aimbot_smooth_mode:
        aimbot.set_aimbot_speed(0.9)
    else:
        aimbot.set_aimbot_speed(2)

def set_aimbot_fov(sender=None, app_data=None):
    global aimbot_fov
    aimbot_fov = dpg.get_value("aimbot_fov_slider")
    aimbot.set_aimbot_fov(aimbot_fov)
    overlay.set_aimbot_fov(aimbot_fov)

def set_aimbot_mode(sender, app_data):
    global aimbot_smooth_mode
    aimbot_smooth_mode = app_data == "smooth"
    aimbot.set_aimbot_mode(aimbot_smooth_mode)
    
    if app_data == "custom":
        dpg.configure_item("aimbot_speed_slider", show=True)
        set_aimbot_speed()
    else:
        dpg.configure_item("aimbot_speed_slider", show=False)

    if aimbot_smooth_mode:
        aimbot.set_aimbot_speed(0.9)
    elif app_data == "plain":
        aimbot.set_aimbot_speed(4)
    else:
        aimbot.set_aimbot_speed(dpg.get_value("aimbot_speed_slider"))

def set_scan_area(sender=None, app_data=None):
    global scan_area_size
    scan_area_size = dpg.get_value("scan_area_slider")
    triggerbot.set_scan_area_size(scan_area_size)
    overlay.set_scan_area_size(scan_area_size)

def toggle_triggerbot(sender, app_data):
    enable = dpg.get_value(sender)
    triggerbot.toggle_triggerbot(enable)
    winsound.Beep(1000 if enable else 500, 200)

def toggle_norecoil(sender, app_data):
    enable = dpg.get_value(sender)
    norecoil.toggle_norecoil()
    winsound.Beep(1000 if enable else 500, 200)

def set_x_recoil(sender=None, app_data=None):
    global x_recoil_compensation
    x_recoil_compensation = dpg.get_value("x_recoil_slider")
    norecoil.horizontal_range = x_recoil_compensation


def set_y_recoil(sender=None, app_data=None):
    global y_recoil_compensation
    y_recoil_compensation = dpg.get_value("y_recoil_slider")
    norecoil.vertical_range = y_recoil_compensation

def is_key_pressed(key_name):
    key_upper = key_name.upper()
    vk_code = key_to_vk.get(key_upper)
    if vk_code is None:
        if len(key_upper) == 1:
            vk_code = ord(key_upper)
        else:
            print(f"Key '{key_name}' not found in mapping.")
            return False
    state = ctypes.windll.user32.GetAsyncKeyState(vk_code)
    return (state & 0x8000) != 0

def assign_key(field):
    assigned_key = None

    mouse_button_mapping = {
        'Button.left': 'Mouse 1',
        'Button.right': 'Mouse 2',
        'Button.middle': 'Mouse 3',
        'Button.x1': 'Mouse 4',
        'Button.x2': 'Mouse 5'
    }

    def on_press(key):
        nonlocal assigned_key
        try:
            if hasattr(key, 'char') and key.char is not None:
                assigned_key = key.char.upper()
            else:
                assigned_key = key.name.upper()
        except AttributeError:
            assigned_key = key.name.upper()
        return False

    def on_click(x, y, button, pressed):
        nonlocal assigned_key
        if pressed:
            button_name = str(button)
            assigned_key = mouse_button_mapping.get(button_name, 'Unknown Mouse Button')
            return False

    try:
        with pynput_keyboard.Listener(on_press=on_press) as keyboard_listener, \
             pynput_mouse.Listener(on_click=on_click) as mouse_listener:
            while assigned_key is None:
                keyboard_listener.join(0.1)
                mouse_listener.join(0.1)

        if assigned_key is None:
            print("No key assigned")
            return

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
        elif field == "norecoil_hold":
            global norecoil_hold_key
            norecoil_hold_key = assigned_key
            dpg.set_value("norecoil_hold_key_field", assigned_key)
        elif field == "norecoil":
            global norecoil_toggle_keys
            norecoil_toggle_keys = [assigned_key]
            dpg.set_value("norecoil_key_field", assigned_key)
    except Exception as e:
        print(f"Error assigning: {e}")

def check_toggle_keys():
    global aimbot_toggled, triggerbot_toggled, norecoil_toggled
    global aimbot_on_hold, triggerbot_on_hold, norecoil_on_hold

    if is_key_pressed(aimbot_toggle_keys[0]):
        if not aimbot_on_hold:
            aimbot_toggled = not aimbot_toggled
            dpg.set_value("aimbot_checkbox", aimbot_toggled)
            aimbot.toggle_aimbot(aimbot_toggled)
            winsound.Beep(1000 if aimbot_toggled else 500, 200)
            aimbot_on_hold = True
    else:
        aimbot_on_hold = False

    if is_key_pressed(triggerbot_toggle_keys[0]):
        if not triggerbot_on_hold:
            triggerbot_toggled = not triggerbot_toggled
            dpg.set_value("triggerbot_checkbox", triggerbot_toggled)
            triggerbot.toggle_triggerbot(triggerbot_toggled)
            winsound.Beep(1000 if triggerbot_toggled else 500, 200)
            triggerbot_on_hold = True
    else:
        triggerbot_on_hold = False

    if is_key_pressed(norecoil_toggle_keys[0]):
        if not norecoil_on_hold:
            norecoil_toggled = not norecoil_toggled
            dpg.set_value("norecoil_checkbox", norecoil_toggled)
            norecoil.toggle_norecoil()
            winsound.Beep(1000 if norecoil_toggled else 500, 200)
            norecoil_on_hold = True
    else:
        norecoil_on_hold = False

    if is_key_pressed(aimbot_hold_key):
        if dpg.get_value("aimbot_on_hold") and not dpg.get_value("aimbot_checkbox"):
            dpg.set_value("aimbot_checkbox", True)
            aimbot.toggle_aimbot(True)
    else:
        if dpg.get_value("aimbot_on_hold") and dpg.get_value("aimbot_checkbox"):
            dpg.set_value("aimbot_checkbox", False)
            aimbot.toggle_aimbot(False)

    if is_key_pressed(triggerbot_hold_key):
        if dpg.get_value("triggerbot_on_hold") and not dpg.get_value("triggerbot_checkbox"):
            dpg.set_value("triggerbot_checkbox", True)
            triggerbot.toggle_triggerbot(True)
    else:
        if dpg.get_value("triggerbot_on_hold") and dpg.get_value("triggerbot_checkbox"):
            dpg.set_value("triggerbot_checkbox", False)
            triggerbot.toggle_triggerbot(False)

    if is_key_pressed(norecoil_hold_key):
        if dpg.get_value("norecoil_on_hold") and not dpg.get_value("norecoil_checkbox"):
            dpg.set_value("norecoil_checkbox", True)
            norecoil.toggle_norecoil()
    else:
        if dpg.get_value("norecoil_on_hold") and dpg.get_value("norecoil_checkbox"):
            dpg.set_value("norecoil_checkbox", False)
            norecoil.toggle_norecoil()

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

def on_aimbot_fov_circle_toggle(sender, app_data):
    overlay.set_aimbot_fov_visible(app_data)
    dpg.configure_item("aimbot_fov_color_field", show=app_data)
    

def on_triggerbot_fov_circle_toggle(sender, app_data):
    overlay.set_triggerbot_fov_visible(app_data)
    dpg.configure_item("triggerbot_fov_color_field", show=app_data)
    
def set_compensation_interval_gui(sender, app_data):
    global compensation_interval
    compensation_interval = app_data
    norecoil.set_compensation_interval(compensation_interval)

def open_color_picker(popup_tag):
    dpg.configure_item(popup_tag, show=True)

def create_color_button_theme(color):
    with dpg.theme() as color_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, color, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color, category=dpg.mvThemeCat_Core)
    return color_theme

def on_aimbot_fov_color_change(sender, app_data):
    color = [int(c * 255) for c in app_data[:3]]

    color_theme = create_color_button_theme(color)
    dpg.bind_item_theme("aimbot_fov_color_field", color_theme)

    overlay.set_aimbot_fov_color(color)
    overlay.update()

def on_triggerbot_fov_color_change(sender, app_data):
    color = [int(c * 255) for c in app_data[:3]]

    color_theme = create_color_button_theme(color)
    dpg.bind_item_theme("triggerbot_fov_color_field", color_theme)

    overlay.set_triggerbot_fov_color(color)
    overlay.update()

def main():
    dpg.create_context()

    apply_custom_theme()

    with dpg.window(tag="primary_window"):
        dpg.set_primary_window("primary_window", True)

        with dpg.tab_bar():
            with dpg.tab(label="Config"):
                dpg.add_combo(label="Monitor Resolution", items=["1280x720", "1920x1080"], callback=set_resolution, tag="resolution_combo")
                dpg.add_combo(label="Colors", items=["ORANGE", "YELLOW", "PURPLE", "RED", "GREEN", "CYAN"], callback=lambda sender, app_data: set_color_range(app_data), tag="color_set_combo")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save Config", callback=lambda: save_config())
                    dpg.add_button(label="Load Config", callback=lambda: load_config())
                    
                dpg.add_text("Dividence v2.9 by secretlay3r", pos=(155, 260))
                dpg.add_text("and community <3", pos=(200, 280))

            with dpg.tab(label="Aimbot"):
                dpg.add_checkbox(label="Enable Aimbot", callback=toggle_aimbot, tag="aimbot_checkbox")
                
                with dpg.group(horizontal=False):
                    dpg.add_combo(label="Preset Mode", items=["smooth", "plain", "custom"], callback=set_aimbot_mode, tag="aimbot_mode_combo")
                    dpg.add_slider_float(label="Custom Speed", default_value=0.9, min_value=0.1, max_value=2.0, callback=set_aimbot_speed, tag="aimbot_speed_slider", show=False)
                    dpg.add_checkbox(label="Show Aimbot FOV Circle", tag="aimbot_fov_circle_checkbox", callback=on_aimbot_fov_circle_toggle)
                    dpg.add_button(tag="aimbot_fov_color_field", label="", width=50, height=20, show=False, callback=lambda: open_color_picker("aimbot_fov_color_popup"))

                    with dpg.popup(parent="aimbot_fov_color_field", modal=False, tag="aimbot_fov_color_popup", mousebutton=dpg.mvMouseButton_Left):
                        dpg.add_color_picker(
                            tag="aimbot_fov_color_picker",
                            default_value=(1.0, 0.0, 0.0, 1.0),
                            no_alpha=True,
                            display_hex=True,
                            width=100,
                            height=100,
                            callback=on_aimbot_fov_color_change
                        )

                    dpg.add_combo(label="Aimbot Region", items=["body", "head", "random"], callback=set_aim_region, tag="aim_region_combo")
                    dpg.add_slider_float(label="Aimbot FOV", default_value=75, min_value=50, max_value=200, callback=set_aimbot_fov, tag="aimbot_fov_slider")
                    dpg.add_checkbox(label="Hold-to-use", tag="aimbot_on_hold")
                    dpg.add_input_text(label="Hold Key", default_value="Mouse 2", readonly=True, tag="aimbot_hold_key_field")
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Set Hold Key", callback=lambda: assign_key("aimbot_hold"))
                    dpg.add_input_text(label="Toggle Key", default_value="F1", readonly=True, tag="aimbot_key_field")
                    dpg.add_button(label="Set Toggle Key", callback=lambda: assign_key("aimbot"))

            with dpg.tab(label="Triggerbot"):
                dpg.add_checkbox(label="Enable Triggerbot", callback=toggle_triggerbot, tag="triggerbot_checkbox")
                
                with dpg.group(horizontal=False):
                    dpg.add_checkbox(label="Show Triggerbot FOV Circle", tag="triggerbot_fov_circle_checkbox", callback=on_triggerbot_fov_circle_toggle)
                    dpg.add_button(tag="triggerbot_fov_color_field", label="", width=50, height=20, show=False, callback=lambda: open_color_picker("triggerbot_fov_color_popup"))
                    
                    with dpg.popup(parent="triggerbot_fov_color_field", modal=False, tag="triggerbot_fov_color_popup", mousebutton=dpg.mvMouseButton_Left):
                        dpg.add_color_picker(
                            tag="triggerbot_fov_color_picker",
                            default_value=(0.0, 1.0, 0.0, 1.0),
                            no_alpha=True,
                            display_hex=True,
                            width=100,
                            height=100,
                            callback=on_triggerbot_fov_color_change
                        )
                        
                    dpg.add_slider_float(label="Triggerbot FOV", default_value=15, min_value=10, max_value=200, callback=set_scan_area, tag="scan_area_slider")
                    dpg.add_checkbox(label="Hold-to-use", tag="triggerbot_on_hold")
                    dpg.add_input_text(label="Hold Key", default_value="Mouse 2", readonly=True, tag="triggerbot_hold_key_field")
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Set Hold Key", callback=lambda: assign_key("triggerbot_hold"))
                    dpg.add_input_text(label="Toggle Key", default_value="F2", readonly=True, tag="triggerbot_key_field")
                    dpg.add_button(label="Set Toggle Key", callback=lambda: assign_key("triggerbot"))

            with dpg.tab(label="NoRecoil"):
                dpg.add_checkbox(label="Enable Recoil Compensation", callback=toggle_norecoil, tag="norecoil_checkbox")
                
                with dpg.group(horizontal=False):
                    dpg.add_slider_float(label="X-Axis Recoil", default_value=2.0, min_value=0, max_value=10, callback=set_x_recoil, tag="x_recoil_slider")
                    dpg.add_slider_float(label="Y-Axis Recoil", default_value=2.0, min_value=0, max_value=10, callback=set_y_recoil, tag="y_recoil_slider")
                    dpg.add_slider_float(
                            label="Compensation Interval",
                            default_value=compensation_interval,
                            min_value=0.01,
                            max_value=0.1,
                            callback=set_compensation_interval_gui,
                            tag="compensation_interval_slider"
                        )
                    dpg.add_checkbox(label="Hold-to-use", tag="norecoil_on_hold")
                    dpg.add_input_text(label="Hold Key", default_value="Mouse 2", readonly=True, tag="norecoil_hold_key_field")
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Set Hold Key", callback=lambda: assign_key("norecoil_hold"))
                    dpg.add_input_text(label="Toggle Key", default_value="F3", readonly=True, tag="norecoil_key_field")
                    dpg.add_button(label="Set Toggle Key", callback=lambda: assign_key("norecoil"))

            with dpg.tab(label="Misc"):
                dpg.add_checkbox(label="Autoswap to Spectre", callback=toggle_autoswap, tag="autoswap_checkbox")
                dpg.add_checkbox(label="Bunny Hop", callback=lambda sender, app_data: bhop.toggle_bhop(app_data), tag="bhop_checkbox")

    aimbot_initial_color = (244, 10, 10)
    triggerbot_initial_color = (10, 244, 10)

    aimbot_color_theme = create_color_button_theme(aimbot_initial_color)
    triggerbot_color_theme = create_color_button_theme(triggerbot_initial_color)

    dpg.bind_item_theme("aimbot_fov_color_field", aimbot_color_theme)
    dpg.bind_item_theme("triggerbot_fov_color_field", triggerbot_color_theme)

    dpg.set_value("aimbot_fov_color_picker", [c / 255.0 for c in aimbot_initial_color] + [1.0])
    dpg.set_value("triggerbot_fov_color_picker", [c / 255.0 for c in triggerbot_initial_color] + [1.0])

    overlay.set_aimbot_fov_color(aimbot_initial_color)
    overlay.set_triggerbot_fov_color(triggerbot_initial_color)

    window_title = generate_random_title()
    dpg.create_viewport(title=window_title, width=510, height=370)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        check_toggle_keys()
        dpg.render_dearpygui_frame()
    overlay.destroy()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
