import winreg
import os
import sys
import shutil

APP_NAME = "Screenshoter"


def get_exe_path():
    if getattr(sys, "frozen", False):
        return sys.executable
    else:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "Screenshoter.exe"
        )


def is_enabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ,
        )
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def enable():
    exe_path = get_exe_path()
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found")
        return False

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE,
    )
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)
    print(f"Added to autostart: {exe_path}")
    return True


def disable():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_ALL_ACCESS,
        )
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print("Removed from autostart")
        return True
    except FileNotFoundError:
        print("Not found in autostart")
        return False


def status():
    if is_enabled():
        print("Status: ENABLED (starts with Windows)")
    else:
        print("Status: DISABLED (does not start with Windows)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "enable":
            enable()
        elif cmd == "disable":
            disable()
        elif cmd == "status":
            status()
        else:
            print("Usage: python autostart.py [enable|disable|status]")
    else:
        status()
        print("\nUsage: python autostart.py [enable|disable|status]")
