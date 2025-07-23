# 🔋 Power Sensor CLI

A Python-based CLI tool to monitor power and performance metrics of a program using Linux system data and cgroups. Ideal for researchers, developers, or anyone profiling energy usage.

---

## 📦 Features

- Detects and stores system info (CPU, OS, counters)
- Runs a target binary in an isolated cgroup
- Collects timestamped power and CPU usage data
- Saves output to a structured JSON file
- Works cleanly within a Python virtual environment
- Automatically handles sudo elevation

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/power_sensor.git
cd power_sensor
2. Set up a Python virtual environment

python3 -m venv sensor_venv
source sensor_venv/bin/activate
3. Install dependencies

pip install -r requirements.txt
⚙️ Setup

Before running, detect your system’s configuration:

power_sensor setup
🚀 Usage
Monitor a binary

power_sensor run /path/to/your/binary -f 1000 -o output/data.json
🧪 Example

power_sensor run ./test_program -f 500 -o output/test_run.json
🔒 Permissions Note

This tool uses:

    /proc, /sys and performance counters

    cgroup v2 for process isolation

As a result, root privileges are needed for accurate monitoring. sudo is invoked automatically by the CLI to re-run the same tool in the correct context.
📁 Output Format

The output JSON will look like this:

[
  {
    "timestamp": "2025-07-23T12:00:00.123Z",
    "power_microwatts": 13890,
    "cpu_usage": 17.4
  },
  ...
]
🧹 Deactivation & Cleanup

After use, you can deactivate the Python environment:

deactivate