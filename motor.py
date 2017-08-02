#!/usr/bin/env python3 


from ev3dev.ev3 import *
# import ev3dev.ev3 as ev3

m = LargeMotor('outB')
m.run_timed(time_sp=3000, speed_sp=500)
