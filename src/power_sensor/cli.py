import argparse
import subprocess
import os
import sys
from power_sensor.setup import setup
from power_sensor.run import run


def main():
    parser = argparse.ArgumentParser(
        prog="power_sensor",
        description="Power Sensor CLI: collect and monitor system power usage"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Setup command
    subparsers.add_parser(
        "setup", help="Detect system info and save counters to JSON"
    )

    # Run command
    run_parser = subparsers.add_parser(
        "run", help="Run a program and collect power usage"
    )
    run_parser.add_argument(
        "executable",
        type=str,
        help="Path to the C/C++ binary to run and monitor",
    )
    run_parser.add_argument(
        "--frequency","-f",
        type=str,
        default=1000,
        help="Sampling frequency (miliseconds)",
    )
    run_parser.add_argument(
        "--output","-o",
        type=str,
        required=True,
        help="Output JSON file path",
    )
    try:
        args = parser.parse_args()
    except:
        print()
    else:
        try:
            if args.command == "setup":
                setup()
            elif args.command == "run":
                if os.geteuid() != 0:
                    print("RUNNING WITH SUDO")
                    python_path = sys.executable
                    cli_entry = os.path.abspath(sys.argv[0])
                    cmd = [
                        "sudo", python_path, cli_entry,
                        "run", args.executable,
                        "--frequency", str(args.frequency),
                        "--output", args.output
                    ]
                    subprocess.run(cmd)
                    return
                run(args.executable, args.frequency, args.output)
        except Exception as e:
            print(f"Error: {e}")


