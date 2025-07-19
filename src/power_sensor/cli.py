import argparse
from power_sensor.setup import setup
from power_sensor.run import run
from power_sensor.check import check
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="power_sensor",
        description="Power Sensor CLI: collect and monitor system power usage"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    #cli check
    subparsers.add_parser(
        "check", help="Check if the cli is operating"
    )
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
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to the program",
    )

    # Custom help command: `power_sensor h` or `power_sensor help`
    help_parser = subparsers.add_parser("h", help="Show help")
    help_parser = subparsers.add_parser("help", help="Show help")

    args = parser.parse_args()

    if args.command == "setup":
        setup()
    elif args.command == "run":
        run(args.executable, args.args)
    elif args.command in {"h", "help"}:
        parser.print_help()
        sys.exit(0)
    elif args.command == "check":
        check()


