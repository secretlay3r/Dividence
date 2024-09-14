import dearpygui.dearpygui as dpg
import triggerbot
import norecoil
import aimbot

aimbot_speed = 0.9  # Default aiming speed
scan_area_size = 20  # Default scan area size for triggerbot

def set_color_range(selected_color):
    triggerbot.set_target_colors([selected_color])
    aimbot.set_target_colors([selected_color])

def toggle_triggerbot(sender, app_data):
    if dpg.get_value(sender):
        triggerbot.toggle_triggerbot(enable=True)
    else:
        triggerbot.toggle_triggerbot(enable=False)

def toggle_norecoil(sender, app_data):
    norecoil.toggle_norecoil()

def toggle_aimbot(sender, app_data):
    if dpg.get_value(sender):
        aimbot.toggle_aimbot(enable=True)
    else:
        aimbot.toggle_aimbot(enable=False)

def set_aimbot_speed(sender, app_data):
    global aimbot_speed
    aimbot_speed = dpg.get_value(sender)
    aimbot.set_aimbot_speed(aimbot_speed)

def set_scan_area(sender, app_data):
    global scan_area_size
    scan_area_size = dpg.get_value(sender)
    triggerbot.set_scan_area_size(scan_area_size)

def apply_custom_theme():
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvCheckbox):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (133, 127, 155))  # Check mark
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30))  # Background
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 50))  # Background on hover
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 70, 70))  # Background when active
        with dpg.theme_component(dpg.mvSliderFloat):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (133, 127, 155))  # Color of slider grab
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (133, 127, 155))  # Color when active
    dpg.bind_theme(theme)

def on_close(sender, app_data):
    dpg.stop_dearpygui()

dpg.create_context()

apply_custom_theme()

with dpg.window(tag="primary_window"):
    dpg.set_primary_window("primary_window", True)
    
    with dpg.group(horizontal=True):
        with dpg.child_window(width=-1, height=-1):
            dpg.add_combo(label="Select Color Set", items=[
                "ORANGE", "YELLOW", "PURPLE", "RED", "GREEN", "CYAN"], 
                callback=lambda sender, app_data: set_color_range(app_data)
            )
            dpg.add_checkbox(label="Aimbot", callback=toggle_aimbot)
            dpg.add_slider_float(label="Aimbot Speed", default_value=0.9, min_value=0.1, max_value=2.0, callback=set_aimbot_speed)
            dpg.add_checkbox(label="Triggerbot", callback=toggle_triggerbot)
            dpg.add_slider_float(label="Scan Area", default_value=20, min_value=10, max_value=200, callback=set_scan_area)
            dpg.add_checkbox(label="Recoil Compensation", callback=toggle_norecoil)
            dpg.add_text("Created by secretlay3r", pos=(145, 250))
            dpg.add_text("Released for free on UnKnoWnCheaTs", pos=(105, 270))

dpg.create_viewport(title='Dividence', width=500, height=350)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()