import win32gui
import win32process
import psutil
import ctypes
from src.GUI import Overlay
from src.skip_song import skip
from src.reopenSpotify import reop
import keyboard
import os
import time
import sys
from ctypes import wintypes
from PySide6.QtCore import QTimer

pending_rehook = False

# Define the RECT structure used by Windows API
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG)
    ]
rect = RECT()
skipScript = None
reopss = None
res = None
overlay=None
current_hwnd = None
is_restarting = False
hook = None
EVENT_MIN = 0x00000001
EVENT_MAX = 0x7FFFFFFF
GetMessageW = ctypes.windll.user32.GetMessageW
TranslateMessage = ctypes.windll.user32.TranslateMessage
DispatchMessageW = ctypes.windll.user32.DispatchMessageW
class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long)
    ]

def find_spotify_main_window(timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        pids = getProcessIDByName()

        for i in pids:
            hwnds = get_hwnds_for_pid(i)
            for hwnd in hwnds:
                if hwnd!=None:
                    l, t, r, b = win32gui.GetWindowRect(hwnd)
                    if r - l >= 200 and b - t >= 200:
                        current_hwnd = hwnd
                        return hwnd
        time.sleep(0.2)
    return None

ctypes.windll.user32.IsWindowVisible.argtypes = [wintypes.HWND]
ctypes.windll.user32.IsWindowVisible.restype = wintypes.BOOL
class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.c_void_p),
        ("message", ctypes.c_uint),
        ("wParam", ctypes.c_void_p),
        ("lParam", ctypes.c_void_p),
        ("time", ctypes.c_uint),
        ("pt", POINT),
    ]

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
WinEventProc = ctypes.WINFUNCTYPE(
    None,
    ctypes.c_void_p,
    ctypes.c_uint,
    ctypes.c_void_p,
    ctypes.c_long,
    ctypes.c_long,
    ctypes.c_ulong,
    ctypes.c_ulong
)
@WinEventProc
def MainLogicFunc(hook, event, hwnd, object_id,child_id, event_thread, event_time):
    if hwnd == None:
        return
    global is_restarting,overlay,res
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    if width < 200 or height < 200:
        return

    if event == 32769 and not is_restarting:
        psutil.Process(os.getpid()).kill()

    overlay.resizeOrMoveOrVisible(res,width,height,rect.left,rect.top, bool(ctypes.windll.user32.IsWindowVisible(hwnd)) )

ctypes.windll.user32.SetWinEventHook.argtypes = [ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,WinEventProc, ctypes.c_ulong,ctypes.c_ulong,   ctypes.c_uint  ]
ctypes.windll.user32.SetWinEventHook.restype = ctypes.c_void_p
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 
def getProcessIDByName():
    _pids = []
    process_name = "Spotify.exe"

    for proc in psutil.process_iter():
        if process_name in proc.name():
            _pids.append(proc.pid)

    return _pids
class xd:
    def __init__(self):
        time.sleep(0.0001)
    def restartKey(self):
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey(overlay.data["prev"], skipScript.prev_song)
        keyboard.add_hotkey(overlay.data["next"], skipScript.skip_song)
        keyboard.add_hotkey(overlay.data["reop"], yperi)


def yperi():
    global pending_rehook
    pending_rehook = True

def do_rehook():
    global is_restarting, hook, current_hwnd

    is_restarting = True
    if hook:
        try:
            ctypes.windll.user32.UnhookWinEvent(hook)
        except Exception:
            pass
        hook = None

    reopss.stop()
    time.sleep(0.25)
    reopss.start()
    time.sleep(1.5)
    keyboard.press('space')
    new_hwnd = find_spotify_main_window(timeout=15)
    if new_hwnd is None:
        is_restarting = False
        return

    _, new_pid = win32process.GetWindowThreadProcessId(new_hwnd)
    current_hwnd = new_hwnd
    hook = ctypes.windll.user32.SetWinEventHook(
        EVENT_MIN, EVENT_MAX, None, MainLogicFunc, new_pid, 0, 0x0000
    )

    ctypes.windll.user32.GetWindowRect(current_hwnd, ctypes.byref(rect))
    w = rect.right - rect.left
    h = rect.bottom - rect.top
    overlay.resizeOrMoveOrVisible(res, w, h, rect.left, rect.top, True)
    is_restarting = False

def check_pending():
    global pending_rehook
    if pending_rehook:
        pending_rehook = False
        do_rehook()
    

if __name__ == '__main__': 
    if hook:
        ctypes.windll.user32.UnhookWinEvent(hook)
        hook = None
    current_hwnd = None
    time.sleep(0.25)
    pids = getProcessIDByName()

    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if hwnd!=None:
                l, t, r, b = win32gui.GetWindowRect(hwnd)
                if r - l >= 200 and b - t >= 200:
                    _, real_pid = win32process.GetWindowThreadProcessId(hwnd)
                    hook = ctypes.windll.user32.SetWinEventHook(EVENT_MIN,EVENT_MAX,None,MainLogicFunc,real_pid,0, 0x0000)
                    current_hwnd = hwnd

                    break
            if hook != None:
                break
    if hook == None:
        psutil.Process(os.getpid()).kill()        
    overlay = Overlay(owner=xd())
    res = overlay.GUI()
    rehook_timer = QTimer()
    rehook_timer.timeout.connect(check_pending)
    rehook_timer.start(200) 
    res.show()
    skipScript = skip()
    reopss = reop()
    keyboard.add_hotkey(overlay.data["prev"], skipScript.prev_song)
    keyboard.add_hotkey(overlay.data["next"], skipScript.skip_song)
    keyboard.add_hotkey(overlay.data["reop"], yperi)
    if(current_hwnd != None):
        ctypes.windll.user32.GetWindowRect(current_hwnd, ctypes.byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        overlay.resizeOrMoveOrVisible(res,width,height,rect.left,rect.top, bool(ctypes.windll.user32.IsWindowVisible(current_hwnd)) )
    
    overlay.run()
    
