#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
m1 = LargeMotor('outC')
m1.run_timed(time_sp=3000, speed_sp=-750)
m2 = LargeMotor('outB')
m2.run_timed(time_sp=3000, speed_sp=-750)

# print("set speed (speed_sp) = " + str(m1.speed_sp))
sleep(1)  # it takes a moment for the motor to start moving
# print("actual speed = " + str(m1.speed))
sleep(5)