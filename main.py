import keyboard
import triggerbot
import norecoil
import aimbot
import winsound
import dearpygui.dearpygui as dpg

aimbot_speed = 0.9
scan_area_size = 20
aimbot_toggle_keys = ["F1"]
triggerbot_toggle_keys = ["F2"]
selected_resolution = "1920x1080"

keys = {
    'a': "A", 'b': "B", 'c': "C", 'd': "D", 'e': "E", 'f': "F", 'g': "G", 'h': "H", 'i': "I", 'j': "J", 'k': "K", 'l': "L", 'm': "M", 'n': "N", 'o': "O", 'p': "P", 'q': "Q", 'r': "R", 's': "S", 't': "T", 'u': "U", 'v': "V", 'w': "W", 'x': "X", 'y': "Y", 'z': "Z",
    '0': "0", '1': "1", '2': "2", '3': "3", '4': "4", '5': "5", '6': "6", '7': "7", '8': "8", '9': "9",
    'space': "SPACE",
    'enter': "ENTER",
    'backspace': "BACKSPACE",
    'tab': "TAB",
    'capslock': "CAPSLOCK",
    'esc': "ESC",
    'minus': "-",
    'equals': "=",
    'leftbracket': "[",
    'rightbracket': "]",
    'backslash': "\\",
    'semicolon': ";",
    'apostrophe': "'",
    'comma': ",",
    'period': ".",
    'forwardslash': "/",
    'f4': "F4", 'f5': "F5", 'f6': "F6", 'f7': "F7", 'f8': "F8", 'f9': "F9", 'f10': "F10", 'f11': "F11", 'f12': "F12",
    'uparrow': "UP ARROW",
    'downarrow': "DOWN ARROW",
    'leftarrow': "LEFT ARROW",
    'rightarrow': "RIGHT ARROW",
    'home': "HOME",
    'end': "END",
    'pageup': "PAGE UP",
    'pagedown': "PAGE DOWN",
    'windows': "WINDOWS KEY",
    'command': "COMMAND",
    'option': "OPTION",
    'fn': "FUNCTION",
    'insert': "INSERT",
    'delete': "DELETE",
    'pausebreak': "PAUSE/BREAK",
    'scrolllock': "SCROLL LOCK",
    'numlock': "NUM LOCK"
}

def set_color_range(selected_color):
    triggerbot.set_target_colors([selected_color])
    aimbot.set_target_colors([selected_color])

def set_resolution(sender, app_data):
    global selected_resolution
    selected_resolution = app_data
    if selected_resolution == "1920x1080":
        aimbot.set_monitor_resolution(1920, 1080)
        triggerbot.set_monitor_resolution(1920, 1080)
    else:
        aimbot.set_monitor_resolution(1280, 720)
        triggerbot.set_monitor_resolution(1280, 720)
        
def toggle_triggerbot(sender, app_data):
    if dpg.get_value(sender):
        triggerbot.toggle_triggerbot(enable=True)
        winsound.Beep(1000, 200)
    else:
        triggerbot.toggle_triggerbot(enable=False)
        winsound.Beep(500, 200)

def toggle_norecoil(sender, app_data):
    norecoil.toggle_norecoil()

def toggle_aimbot(sender, app_data):
    if dpg.get_value(sender):
        aimbot.toggle_aimbot(enable=True)
        winsound.Beep(1000, 200)
    else:
        aimbot.toggle_aimbot(enable=False)
        winsound.Beep(500, 200)

def set_aimbot_speed(sender, app_data):
    global aimbot_speed
    aimbot_speed = dpg.get_value(sender)
    aimbot.set_aimbot_speed(aimbot_speed)

def set_scan_area(sender, app_data):
    global scan_area_size
    scan_area_size = dpg.get_value(sender)
    triggerbot.set_scan_area_size(scan_area_size)

def assign_key(field):
    key = keyboard.read_key()
    assigned_key = keys.get(key.lower(), key.upper())
    if field == "aimbot":
        global aimbot_toggle_keys
        aimbot_toggle_keys = [assigned_key]
        dpg.set_value("aimbot_key_field", assigned_key)
    elif field == "triggerbot":
        global triggerbot_toggle_keys
        triggerbot_toggle_keys = [assigned_key]
        dpg.set_value("triggerbot_key_field", assigned_key)

def check_toggle_keys():
    if aimbot_toggle_keys and keyboard.is_pressed(aimbot_toggle_keys[0].lower()):
        current_value = dpg.get_value("aimbot_checkbox")
        dpg.set_value("aimbot_checkbox", not current_value)
        toggle_aimbot("aimbot_checkbox", None)
    
    if triggerbot_toggle_keys and keyboard.is_pressed(triggerbot_toggle_keys[0].lower()):
        current_value = dpg.get_value("triggerbot_checkbox")
        dpg.set_value("triggerbot_checkbox", not current_value)
        toggle_triggerbot("triggerbot_checkbox", None)

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
    
    with dpg.group(horizontal=True):
        with dpg.child_window(width=-1, height=-1):
            dpg.add_combo(label="Select Monitor Resolution", items=["1280x720", "1920x1080"], 
                callback=set_resolution)
        
            dpg.add_combo(label="Select Color Set", items=[
                "ORANGE", "YELLOW", "PURPLE", "RED", "GREEN", "CYAN"], 
                callback=lambda sender, app_data: set_color_range(app_data)
            )
        
            dpg.add_checkbox(label="Aimbot", callback=toggle_aimbot, tag="aimbot_checkbox")
            dpg.add_slider_float(label="Aimbot Speed", default_value=0.9, min_value=0.1, max_value=2.0, callback=set_aimbot_speed)
            dpg.add_input_text(label="Aimbot Key", default_value="F1", readonly=True, tag="aimbot_key_field")
            dpg.add_button(label="Set Aimbot Key", callback=lambda: assign_key("aimbot"))

            dpg.add_checkbox(label="Triggerbot", callback=toggle_triggerbot, tag="triggerbot_checkbox")
            dpg.add_slider_float(label="Scan Area", default_value=20, min_value=10, max_value=200, callback=set_scan_area)
            dpg.add_input_text(label="Triggerbot Key", default_value="F2", readonly=True, tag="triggerbot_key_field")
            dpg.add_button(label="Set Triggerbot Key", callback=lambda: assign_key("triggerbot"))

            dpg.add_checkbox(label="Recoil Compensation", callback=toggle_norecoil)

            dpg.add_text("Created by secretlay3r", pos=(155, 260))
            dpg.add_text("Released for free on UnKnoWnCheaTs", pos=(115, 280))

dpg.create_viewport(title='Dividence', width=510, height=370)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    check_toggle_keys()
    dpg.render_dearpygui_frame()

dpg.destroy_context()
