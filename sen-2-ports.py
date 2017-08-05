#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

# Connect TWO touch sensors to BOTH sensor ports 1 and 2
# and check they are both connected.

ts1 = TouchSensor('in1')
assert ts1.connected, "Connect a touch sensor to sensor port 1"

ts2 = TouchSensor('in2')
assert ts2.connected, "Connect a touch sensor to sensor port 2"

while True:    # Stop this program with Ctrl-C
    Leds.set_color(Leds.LEFT, (Leds.GREEN, Leds.RED)[ts1.value()])
    Leds.set_color(Leds.RIGHT, (Leds.GREEN, Leds.RED)[ts2.value()])

# Stop program with Ctrl-C
