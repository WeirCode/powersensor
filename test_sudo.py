import os
from src.power_sensor.run import run
print("Running as uid:", os.geteuid())
print("Python executable:", __file__)
try:
    run("test/main", 1000, "output/test.json")
except Exception as e:
    print(e)
