import subprocess
import time
p = subprocess.run(["xdotool", "mousemove", "450", "250"])
p = subprocess.run(["xdotool", "mousedown", "1"])
time.sleep(0.5)
p = subprocess.run(["xdotool", "mouseup", "1"])

p.check_returncode()