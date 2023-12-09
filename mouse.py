import random
import subprocess
import time


def _run(command: str):
    command = "xdotool " + command
    p = subprocess.run(command.split(" "))
    p.check_returncode()


def move_mouse_to_default_spot():
    _run("mousemove 450 250")


def mousedown():
    _run("mousedown 1")


def mouseup():
    _run("mouseup 1")


def slow_click_random():
    sleep_time = random.random()
    sleep_time = min(0.1, sleep_time)
    sleep_time = max(0.2, sleep_time)
    mousedown()
    time.sleep(sleep_time)
    mouseup()


def click():
    _run("click 1")
