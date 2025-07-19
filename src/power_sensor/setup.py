import platform
import os
import json
import psutil
import cpuinfo
from pathlib import Path

def setup():
    print("Setup started...")
    print("Detecting Operating System...")
    os_name = detect_os()
    print(f"Detected OS: {os_name}")
    info = cpuinfo.get_cpu_info()

def write_to_json():
    

def detect_os():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "macOS"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"
