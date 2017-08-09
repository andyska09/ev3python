#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

def measure_and_save_color(say_prompt, touch_sensor, cl, file):
    Sound.speak(say_prompt).wait()
    color = cl.value()
    while not touch_sensor.value():
        color = cl.value()
    print(color)
    text_file.write("%s\n" % color)
    return

text_file = open("color.txt", "w")
ts = TouchSensor()
cl = ColorSensor()
assert cl.connected, "Connect a color sensor to any sensor port"
cl.mode = 'COL-REFLECT'

measure_and_save_color('Show me white', ts, cl, text_file)
measure_and_save_color('Show me black', ts, cl, text_file)

text_file.close()
