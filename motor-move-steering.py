#!/usr/bin/env python3


import ev3dev.ev3 as ev3
from time import sleep


m_b = ev3.LargeMotor('outB') 
m_c = ev3.LargeMotor('outC')

b = 0
tp = 500
st = input("steering: ")
t = input("time: ")
b = tp + int(st)
print(b)

print('motory jedou')

m_b.run_timed(time_sp=t, speed_sp=b, stop_action='brake')
m_c.run_timed(time_sp=t, speed_sp=tp, stop_action='brake')
m_b.wait_while('running')
m_c.wait_while('running')
print('konec')
#m = LargeMotor('outB')
#m.run_timed(time_sp=3000, speed_sp=500)
