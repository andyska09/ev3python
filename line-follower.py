#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

ts = TouchSensor()
m_b = LargeMotor('outB')
m_c = LargeMotor('outC')
m_b.run_forever(speed_sp=900)
m_c.run_forever(speed_sp=-900)
i = 0
while not ts.value():    # Stop program by pressing touch sensor button
    print(i)
    i = i + 1
m_b.stop(stop_action="hold")
m_c.stop(stop_action="hold")
