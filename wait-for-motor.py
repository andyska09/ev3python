#!/usr/bin/env python3
from ev3dev.ev3 import *

motor = LargeMotor('outC')
motor.run_timed(time_sp=3000, speed_sp=-750, stop_action='brake')
motor.wait_while('running')

Sound.beep()