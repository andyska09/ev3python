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
m_b.run_forever(speed_sp=900)
m_c.run_forever(speed_sp=-900)

while not ts.value():    # Stop program by pressing touch sensor button
    print(cl.value())
    sleep(0.5)

m_b.stop(stop_action="hold")
m_c.stop(stop_action="hold")
