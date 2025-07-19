#!/bin/bash

# Exit on error except in specific cases
set -euo pipefail

function check_command() {
    command -v "$1" >/dev/null 2>&1 || {
    echo >&2 "Error: '$1' is not installed or not in PATH."
    exit 1
    }
}

echo "Checking dependencies..."

check_command python3
check_command pip

echo "Creating virtual environment..."
python3 -m venv sensor_venv || {
    echo "Failed to create virtual environment."
    exit 1
}

echo "Activating virtual environment..."
source sensor_venv/bin/activate || {
    echo "Failed to activate virtual environment."
    exit 1
}

echo "Upgrading pip..."
pip install --upgrade pip || {
    echo "Failed to upgrade pip."
    exit 1
}

echo "Installing project in editable mode..."
pip install -e . || {
    echo "Failed to install the project."
    exit 1
}

echo "✅ Virtual environment is ready."
echo "CLI power_sensor <command> is now ready to use"
