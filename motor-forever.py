#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

m_b = LargeMotor('outB')
m_c = LargeMotor('outC')

ts = TouchSensor()
assert ts.connected, "Connect a touch sensor to any port"

x = 100 
while not ts.value():
    m_b.run_forever(speed_sp=x)
    m_c.run_forever(speed_sp=x)
    x = 1 + x
m_c.stop(stop_action="brake")
m_b.stop(stop_action="brake")