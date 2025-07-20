import argparse
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

    args = parser.parse_args()

    if args.command == "setup":
        try:
            setup()
        except:
            print("There was an error running the setup")
    elif args.command == "run":
        try:
            run(args.exe,args.frequency)
        except:
            print("There was an error running the run command")


