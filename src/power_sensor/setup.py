import platform
import os
import json
import psutil
import cpuinfo
from pathlib import Path
import subprocess

def setup():
    print("Setup started...")
    print("Detecting Operating System...")
    try:
        os_name = detect_os()
    except Exception as e:
        print(e,"Could not detect os python platform library may not be connected")
        return
    print(f"Detected OS: {os_name}")
    print("Gathering info")
    if os_name == "Linux":
        gatherLinux()
    elif os_name == "Windows":
        return
    elif os_name == "macOS":
        return

def gatherLinux():
    try:
        data = {
            "os": get_os(),
            "cpu": get_cpu_info(),
            "cpu_stats": get_cpu_stats(),
            "features": {
                "msr": check_msr_support(),
                "perf": check_perf_support(),
                "rapl_domains": detect_rapl_domains(),
                "cgroup_version": get_cgroup_version(),
                "pmu_events": get_pmu_events()
            }
        }
    except Exception as e:
        print(f"Error collecting data {e}")
        return
    print(data)
    try:
        # Use the path relative to the script file location
        base_dir = Path(__file__).resolve().parent
        info_path = base_dir / "system_info" / "info.json"
        info_path.parent.mkdir(parents=True, exist_ok=True)
        with open(info_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Collected system info to {info_path}")
    except Exception as e:
        print(f"Couldn't save file: {e}")

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

def get_os():
    try:
        result = subprocess.run(
            ["uname", "-a"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        os_info = result.stdout.strip().split()
        return os_info
    except subprocess.CalledProcessError as e:
        print("Error collecting OS info", e)
        return []

def cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        "brand": info.get("brand_raw"),
        "arch": info.get("arch"),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "flags": info.get("flags"),
        "l2_cache_size": info.get("l2_cache_size"),
        "l3_cache_size": info.get("l3_cache_size")
    }

def get_pmu_events():
    base_dir = Path(__file__).resolve().parent
    info_path = base_dir / "system_info" / "perf_raw.json"
    info_path.parent.mkdir(parents=True, exist_ok=True)
    output_file = info_path
    # Step 1: Run `perf list -j -o <file>`
    try:
        subprocess.run(
            ["perf", "list", "-j", "-o", str(output_file)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print("Failed to run `perf list -j`.")
        return {}
    # Step 2: Parse the generated JSON
    try:
        with open(output_file, "r") as f:
            events = json.load(f)
    except Exception as e:
        print(f"Failed to read or parse {output_file}: {e}")
        return {}
    # Step 3: Extract and return {EventName: Encoding} dictionary
    event_dict = {}
    for event in events:
        name = event.get("EventName")
        encoding = event.get("Encoding")
        etype = event.get("EventType")
        if name and encoding and (etype == "Kernel PMU event"):
            event_dict[name] = encoding
    return event_dict

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        "brand": info.get("brand_raw"),
        "arch": info.get("arch"),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "flags": info.get("flags"),
        "l2_cache_size": info.get("l2_cache_size"),
        "l3_cache_size": info.get("l3_cache_size")
    }

def get_cpu_stats():
    freqs = psutil.cpu_freq(percpu=True)
    usage = psutil.cpu_percent(percpu=True)
    temps = psutil.sensors_temperatures(fahrenheit=False)
    core_data = []
    for i, f in enumerate(freqs):
        core_data.append({
            "core": i,
            "frequency_mhz": f.current,
            "usage_percent": usage[i]
        })
    temp_data = {}
    for sensor, readings in temps.items():
        temp_data[sensor] = [
            {"label": r.label, "temp_c": r.current} for r in readings
        ]
    return {
        "cores": core_data,
        "temperatures": temp_data
    }

def detect_rapl_domains():
    domains = []
    powercap_path = Path("/sys/class/powercap/")
    if not powercap_path.exists():
        return domains
    for domain in powercap_path.glob("intel-rapl:*"):
        name_path = domain / "name"
        if name_path.exists():
            try:
                domain_name = name_path.read_text().strip()
                domains.append(domain_name)
            except:
                continue
    return domains

def check_msr_support():
    return os.path.exists("/dev/cpu/0/msr")

def check_perf_support():
    try:
        out = os.popen("perf list").read()
        return "cpu-cycles" in out
    except:
        return False

def get_cgroup_version():
    if os.path.exists("/sys/fs/cgroup/cgroup.controllers"):
        return 2
    elif os.path.exists("/sys/fs/cgroup/memory/"):
        return 1
    return 0
