#!/bin/bash
set -e

echo "Creating virtual environment..."
python3 -m venv sensor_venv

echo "Activating..."
source sensor_venv/bin/activate

pip install --upgrade pip

pip install -e .

echo "Virtual Environment ready"
