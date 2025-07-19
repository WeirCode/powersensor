Run
PreRequisites
Python needs to be installed
Setup for Linux
sudo apt install python3 python3-pip python3-venv

Sets up virtual environment and power_sensor cli tool
source setup_venv.sh

Runs the setup which gathers information about computer
power_sensor setup

runs the sensor on a target
power_sensor run -t <target> -f <frequency> ...
