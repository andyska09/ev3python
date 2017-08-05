#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

# Connect EV3 color sensor and check connected.

cl = ColorSensor()
assert cl.connected, "Connect a color sensor to any sensor port"

# Put the color sensor into COL-REFLECT mode
# to measure reflected light intensity.
# In this mode the sensor will return a value between 0 and 100
cl.mode = 'COL-REFLECT'
i = 0
while i < 100:
    print(cl.value())
    sleep(0.5)
    i = i + 1
# I get max 80 with white paper, 3mm separation
# and 5 with black plastic, same separation
