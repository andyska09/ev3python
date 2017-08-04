#!/usr/bin/env python3 


import ev3dev.ev3 as ev3
from time import sleep

m = ev3.LargeMotor('outB')

m.run_to_rel_pos(position_sp=360, speed_sp=1000, stop_action="hold")

sleep(5)   # Give the motor time to move

#m = LargeMotor('outB')
#m.run_timed(time_sp=3000, speed_sp=500)
