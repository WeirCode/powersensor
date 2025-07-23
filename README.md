# Power Sensor

A Python-based CLI tool to monitor power and performance metrics of a program. Ideal for researchers, developers, or anyone profiling energy usage.

## Prerequisites

- Python installed

## 🛠️ Installation (Linux)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/power_sensor.git
cd power_sensor
```
### 2. Run the virtualenv setup

```bash
source setup_venv.sh
```
### 3. Run the power_sensor tool 
- power_sensor {,setup,run} -h/--help
- Run the setup this saves computer information to a json file and uses it later
```bash
power_sensor setup
```
- ❗️Don't run this command with sudo. The command requires sudo but don't run directly it will crash. Run the function below and it reruns correctly with sudo
- Run the run command this runs the sensor on your target(executable)
```bash
power_sensor run <executable full path> -f <frequency(ms) default:1000> -o <output json path>
```

### 4. Output
- The setup command returns two output files in the system_info folder
- perf_raw.json
Example
[
    {
	"Unit": "cpu_atom",
	"EventName": "bus-cycles",
	"EventAlias": "cpu_atom/bus-cycles/",
	"EventType": "Kernel PMU event",
	"Encoding": "cpu_atom/event=0x3c,umask=0x1/"
    },
    ...
]
- info.json
{
  "os": [
    ],
  "cpu": {
    "brand":,
    "arch":,
    "physical_cores":,
    "logical_cores":,
    "flags": [
        ],
    "l2_cache_size":,
    "l3_cache_size":
  },
  "cpu_stats": {
    "cores": [
        ],
    "temperatures": {
    }
  },
  "features": {
    "msr": ,
    "perf": ,
    "rapl_domains": [
    ],
    "cgroup_version":,
    "pmu_events": {
  }
  }
}
-run command produces output to specified output folder
Example
[
    {
    "timestamp": "2025-07-23T14:42:36.289273",
    "cgroup_cpu_ticks": 1,
    "system_cpu_ticks": 165445,
    "num_pids": 1
    },
    ...
]
## Deactivation
After use, you can deactivate the Python environment:
```bash
deactivate
```