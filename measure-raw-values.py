#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

cl_left = ColorSensor("in1") #left cl sensor
cl_middle = ColorSensor("in2") #middle cl sensor
cl_right = ColorSensor("in3") #right cl sensor
ts = TouchSensor()

cl_left.mode = 'COL-REFLECT'
cl_middle.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'
assert ColorSensor().connected, "Connect a color sensor to any sensor port"
assert ts.connected, "Connect a touch sensor to any sensor port"

while not ts.value():
    print("l:%d m:%d r:%d\n" % (cl_left.value(), cl_middle.value(), cl_right.value()))

