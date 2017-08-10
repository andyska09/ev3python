#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

cl = ColorSensor()
ts = TouchSensor()
assert cl.connected, "Connect a color sensor to any sensor port"
assert ts.connected, "Connect a touch sensor to any sensor port"

cl.mode = 'COL-REFLECT'

m_b = LargeMotor('outB')
m_c = LargeMotor('outC')

with open('color.txt') as f:
    white = int(f.readline())
    print(white)
    black = int(f.readline())
    print(black)


kp = 1
tp = 500
corr = 0
target = (white-black)/2+black

while not ts.value():    # Stop program by pressing touch sensor button
    corr = (target - cl.value())*kp
    b = tp + corr*10
    m_b.run_forever(speed_sp = b)
    m_c.run_forever(speed_sp = tp)
m_b.stop(stop_action="hold")
m_c.stop(stop_action="hold")
