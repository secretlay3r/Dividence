import threading
import win32api
import win32con
import win32gui

from utils import *

class OverlayWindow:
    def __init__(self):
        self.hInstance = win32api.GetModuleHandle(None)
        self.className = generate_random_title()
        self.aimbot_fov = 75
        self.scan_area_size = 15

        wndClass = win32gui.WNDCLASS()
        wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc = self.wndProc
        wndClass.hInstance = self.hInstance
        wndClass.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wndClass.hbrBackground = 0
        wndClass.lpszClassName = self.className

        wndClassAtom = win32gui.RegisterClass(wndClass)

        exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST
        style = win32con.WS_POPUP | win32con.WS_BORDER

        self.width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        self.hwnd = win32gui.CreateWindowEx(
            exStyle,
            wndClassAtom,
            self.className,
            style,
            0, 0,
            self.width,
            self.height,
            None,
            None,
            self.hInstance,
            None
        )

        win32gui.SetLayeredWindowAttributes(self.hwnd, 0x000000, 0, win32con.LWA_COLORKEY)

        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

        self.aimbot_fov_visible = False
        self.aimbot_fov_color = (255, 0, 0)
        self.triggerbot_fov_visible = False
        self.triggerbot_fov_color = (0, 255, 0)

        self.running = True

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def wndProc(self, hwnd, msg, wParam, lParam):
        if msg == win32con.WM_PAINT:
            self.on_paint(hwnd)
            return 0
        elif msg == win32con.WM_ERASEBKGND:
            hdc = wParam
            rect = win32gui.GetClientRect(hwnd)
            brush = win32gui.CreateSolidBrush(0x000000)
            win32gui.FillRect(hdc, rect, brush)
            win32gui.DeleteObject(brush)
            return 1

        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        else:
            return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

    def on_paint(self, hwnd):
        hdc, ps = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        brush = win32gui.CreateSolidBrush(0x000000)
        win32gui.FillRect(hdc, rect, brush)
        win32gui.DeleteObject(brush)
                
        if self.aimbot_fov_visible:
            self.draw_fov_circle(hdc, self.aimbot_fov_color, self.aimbot_fov)
        if self.triggerbot_fov_visible:
            self.draw_fov_circle(hdc, self.triggerbot_fov_color, self.scan_area_size)
            
        win32gui.EndPaint(hwnd, ps)

    def draw_fov_circle(self, hdc, color, radius):
        x = self.width // 2
        y = self.height // 2

        r, g, b = color
        pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(r, g, b))
        old_pen = win32gui.SelectObject(hdc, pen)

        brush = win32gui.GetStockObject(win32con.NULL_BRUSH)
        old_brush = win32gui.SelectObject(hdc, brush)

        win32gui.Ellipse(hdc, int(x - radius), int(y - radius), int(x + radius), int(y + radius))

        win32gui.SelectObject(hdc, old_pen)
        win32gui.DeleteObject(pen)
        win32gui.SelectObject(hdc, old_brush)
        win32gui.DeleteObject(brush)



    def update(self):
        win32gui.InvalidateRect(self.hwnd, None, True)

    def run(self):
        while self.running:
            win32gui.PumpWaitingMessages()

    def destroy(self):
        self.running = False
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        self.thread.join()

    def set_aimbot_fov_visible(self, visible):
        self.aimbot_fov_visible = visible
        self.update()

    def set_triggerbot_fov_visible(self, visible):
        self.triggerbot_fov_visible = visible
        self.update()


    def set_aimbot_fov_color(self, color):
        self.aimbot_fov_color = color
        self.update()

    def set_triggerbot_fov_color(self, color):
        self.triggerbot_fov_color = color
        self.update()
        
    def set_aimbot_fov(self, fov):
        self.aimbot_fov = fov
        self.update()

    def set_scan_area_size(self, size):
        self.scan_area_size = size
        self.update()