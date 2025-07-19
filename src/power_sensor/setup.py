import platform
import subprocess
import sys
import os
import urllib.request
import tarfile

def setup():
    print("Setup started...")
    print("Detecting Operating System...")
    os_name = detect_os()
    print(f"Detected OS: {os_name}")
    print("Building osquery")
    try:
        build_osquery()
    except Exception as e:
        print(f"Setup failed: {e}")

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

def build_osquery():
    # Get the directory of this Python file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the shell script
    shell_script = os.path.join(base_dir, "setup_osquery.sh")

    print(f"Running osquery source build script at: {shell_script}")
    
    try:
        subprocess.run(["bash", shell_script], check=True)
        print("osquery build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build script failed with error: {e}")

