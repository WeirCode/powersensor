Run
source setup_venv.sh "Sets up virtual environment and power_sensor cli tool"
power_sensor setup "Runs the setup which gathers information about computer 
and saves in json files"
power_sensor run -t <target> -f <frequency> ... "runs the sensor on a target
exe with other flags"
