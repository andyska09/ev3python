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
with open('color.txt') as f:
    white = int(f.readline())
    print(white)
    black = int(f.readline())
    print(black)
target = (white - black) / 2

while not ts.value():
    err = target - cl_middle.value()       
    print(err)
