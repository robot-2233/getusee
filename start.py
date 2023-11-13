import winreg
import socket
import os
import sys
import subprocess
import platform


def is_port_in_use(port: int or str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0


def get_chrome_path(system: str):
    if 'win' in system:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
            path, _ = winreg.QueryValueEx(key, "")
            return path
        except Exception as e:
            print('Chrome Path Error!')
            return None
    elif 'mac' in system:
        try:
            path = subprocess.check_output(["which", "google-chrome"]).decode("utf-8").strip()
            return path
        except Exception as e:
            print('Chrome Path Error!')
            return None
    else:
        return None


def get_chromedriver_path(system: str):
    path = sys.executable
    driver_directory = path.rsplit('\\', 1)[0] if '\\' in path else path
    if 'win' in system:
        driver_directory = os.path.join(driver_directory, 'chromedriver.exe')
    elif 'mac' in system:
        driver_directory = os.path.join(driver_directory, 'chromedriver')
    else:
        print('Unknown System')
        return None
    if os.path.exists(driver_directory) and os.path.isfile(driver_directory):
        return driver_directory
    else:
        print('[INFO]:Chrome driver not in PATH')
        return None


def see_system():
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        return 'win32'
    elif sys.platform.startswith('linux'):
        return 'linux64'
    elif sys.platform.startswith('darwin'):
        return 'mac_arm64' if platform.machine() == 'arm64' else 'mac64'


def set_global_proxy(ip: str, port: str):
    os.environ["http_proxy"] = f"http://{ip}:{port}"
    os.environ["https_proxy"] = f"http://{ip}:{port}"
