import subprocess
import time
import json
import os
from datetime import datetime
from tempfile import TemporaryDirectory
from pathlib import Path

def run(executable_path, frequency_ms, output_path):
    frequency_sec = int(frequency_ms) / 1000.0
    samples = []

    process, cg_path = start_tracked_process(executable_path)

    try:
        while process.poll() is None:
            sample = collect_sample(cg_path)
            samples.append(sample)
            time.sleep(frequency_sec)
    finally:
        process.wait()  # Ensure cleanup
        if os.path.exists(cg_path):
            os.rmdir(cg_path)

    # Save results
    with open(output_path, "w") as f:
        json.dump(samples, f, indent=2)

def start_tracked_process(executable_path):
    """Start the target program in a new cgroup and return its PID."""
    with TemporaryDirectory(prefix="power_sensor_") as cg_path:
        cg_path = Path("/sys/fs/cgroup") / f"power_sensor_{os.getpid()}"
        os.makedirs(cg_path, exist_ok=True)
        # Start the process
        process = subprocess.Popen([executable_path])
        pid = process.pid
        # Add the PID to the cgroup
        tasks_file = cg_path / "cgroup.procs"
        with open(tasks_file, "w") as f:
            f.write(str(pid))
        return process, cg_path

def collect_sample(cg_path):
    """Return timestamped CPU usage of cgroup and total system."""
    pids = get_cgroup_pids(cg_path)
    timestamp = datetime.now().isoformat()

    cgroup_total = sum(read_proc_stat(pid) for pid in pids)
    system_total = sum(read_proc_stat(pid) for pid in os.listdir("/proc") if pid.isdigit())

    return {
        "timestamp": timestamp,
        "cgroup_cpu_ticks": cgroup_total,
        "system_cpu_ticks": system_total,
        "num_pids": len(pids),
    }

def read_proc_stat(pid):
    """Return %CPU from /proc/[pid]/stat."""
    try:
        with open(f"/proc/{pid}/stat", "r") as f:
            stat = f.read().split()
        utime = int(stat[13])
        stime = int(stat[14])
        return utime + stime
    except Exception:
        return 0

def get_cgroup_pids(cg_path):
    """Return list of PIDs in the cgroup."""
    tasks_file = cg_path / "cgroup.procs"
    try:
        with open(tasks_file, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def start_tracked_process(executable_path):
    """Start the target program in a new cgroup and return its PID."""
    with TemporaryDirectory(prefix="power_sensor_") as cg_path:
        cg_path = Path("/sys/fs/cgroup") / f"power_sensor_{os.getpid()}"
        os.makedirs(cg_path, exist_ok=True)

        # Start the process
        process = subprocess.Popen([executable_path])
        pid = process.pid

        # Add the PID to the cgroup
        tasks_file = cg_path / "cgroup.procs"
        with open(tasks_file, "w") as f:
            f.write(str(pid))

        return process, cg_path