import subprocess
import time
import json
import os
from datetime import datetime
from tempfile import TemporaryDirectory
from pathlib import Path
import sys

def validate_inputs(executable_path, frequency_ms):
    if not os.path.exists(executable_path):
        raise FileNotFoundError(f"Executable '{executable_path}' does not exist.")
    if not os.access(executable_path, os.X_OK):
        raise PermissionError(f"File '{executable_path}' is not executable.")
    try:
        frequency_ms = int(frequency_ms)
        if frequency_ms <= 0:
            raise ValueError("Frequency must be positive")
    except ValueError:
        raise ValueError("Frequency must be a positive integer (milliseconds).")
    return frequency_ms

def start_tracked_process(executable_path):
    cg_name = f"power_sensor_{os.getpid()}"
    cg_path = Path("/sys/fs/cgroup") / cg_name
    try:
        os.makedirs(cg_path, exist_ok=True)
        process = subprocess.Popen([executable_path])
        with open(cg_path / "cgroup.procs", "w") as f:
            f.write(str(process.pid))
        return process, cg_path
    except PermissionError as e:
        raise PermissionError("Cannot create or write to cgroup. Try running with sudo.") from e
    except Exception as e:
        raise RuntimeError(f"Error starting process or setting up cgroup: {e}") from e

def get_cgroup_pids(cg_path):
    try:
        with open(cg_path / "cgroup.procs", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception:
        return []

def read_proc_stat(pid):
    try:
        with open(f"/proc/{pid}/stat", "r") as f:
            stat = f.read().split()
        utime = int(stat[13])
        stime = int(stat[14])
        return utime + stime
    except Exception:
        return 0


def collect_sample(cg_path):
    timestamp = datetime.now().isoformat()
    pids = get_cgroup_pids(cg_path)
    cgroup_total = sum(read_proc_stat(pid) for pid in pids)
    system_total = sum(
        read_proc_stat(pid) for pid in os.listdir("/proc") if pid.isdigit()
    )
    return {
        "timestamp": timestamp,
        "cgroup_cpu_ticks": cgroup_total,
        "system_cpu_ticks": system_total,
        "num_pids": len(pids),
    }


def run(executable_path, frequency_ms, output_path):
    print("Validating input")
    frequency_ms = validate_inputs(executable_path, frequency_ms)
    frequency_sec = frequency_ms / 1000.0
    samples = []
    print("Starting Process")
    process, cg_path = start_tracked_process(executable_path)
    try:
        while process.poll() is None:
            samples.append(collect_sample(cg_path))
            time.sleep(frequency_sec)
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")
    finally:
        process.wait()
        try:
            os.rmdir(cg_path)
        except Exception:
            pass  # Ignore cleanup error
    try:
        with open(output_path, "w") as f:
            json.dump(samples, f, indent=2)
        print(f"\n✅ Output saved to: {output_path}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)
