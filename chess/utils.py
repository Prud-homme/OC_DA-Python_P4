import os
import time

from .logger import loglevel


def clear_display():
    return os.system("cls")


def pause():
    input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


def autopause():
    if loglevel in ["DEBUG", "INFO"]:
        time.sleep(1.5)
    else:
        time.sleep(0)
