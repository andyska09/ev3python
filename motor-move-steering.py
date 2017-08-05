#!/usr/bin/env python3 


import ev3dev.ev3 as ev3
from time import sleep


m_b = ev3.LargeMotor('outB')
m_c = ev3.LargeMotor('outC')

m_b.run_to_rel_pos(position_sp=360, speed_sp=1000, stop_action="hold")
m_c.run_to_rel_pos(position_sp=-360, speed_sp=1000, stop_action="hold")
ev3.Sound.beep()
m_b.wait_while('running')
m_c.wait_while('running')
print('konec')
#m = LargeMotor('outB')
#m.run_timed(time_sp=3000, speed_sp=500)
