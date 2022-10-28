import subprocess
import time


for i in range(10):
    subprocess.Popen(["python", "bot/main.py"])
    time.sleep(1)