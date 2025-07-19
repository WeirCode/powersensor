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
    print("Gathering info")
    data = {
        "cpu": get_cpu_info(),
        "cpu_stats": get_cpu_stats(),
        "rapl": detect_rapl_sysfs(),
        "features": {
            "msr": check_msr_support(),
            "perf": check_perf_support(),
            "cgroup_version": get_cgroup_version()
        }
    }
    print(data)
    with open("system_info/info.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Collected system info to info.json")
    
def cpu_info():
    get = cpuinfo.get_cpu_info()
    return {
        "brand": info.get("brand_raw"),
        "arch": info.get("arch"),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "flags": info.get("flags"),
        "l2_cache_size": info.get("l2_cache_size"),
        "l3_cache_size": info.get("l3_cache_size")
    }
    
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

def detect_rapl_sysfs():
    domains = {}
    powercap_path = Path("/sys/class/powercap/")
    if not powercap_path.exists():
        return domains
    for domain in powercap_path.glob("intel-rapl:*"):
        domain_info = {}
        name_path = domain / "name"
        energy_path = domain / "energy_uj"
        max_energy_path = domain / "max_energy_range_uj"
        if name_path.exists() and energy_path.exists():
            domain_name = name_path.read_text().strip()
            domain_info["energy_uj"] = int(energy_path.read_text())
            if max_energy_path.exists():
                domain_info["max_energy_range_uj"] = int(max_energy_path.read_text())
            subdomains = {}
            for sub in domain.glob("intel-rapl:*"):
                subname_path = sub / "name"
                subenergy_path = sub / "energy_uj"
                if subname_path.exists() and subenergy_path.exists():
                    sub_name = subname_path.read_text().strip()
                    subdomains[sub_name] = int(subenergy_path.read_text())
            if subdomains:
                domain_info["subdomains"] = subdomains
            domains[domain_name] = domain_info
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
