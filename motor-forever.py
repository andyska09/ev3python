#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

m_b = LargeMotor('outB')
m_c = LargeMotor('outC')

# m_b.stop(stop_action="hold")
# m_c.stop(stop_action="hold")

print("0 start")
m_b.run_forever(speed_sp=600)
m_c.run_forever(speed_sp=600)
sleep(2)
# print("1 before hold")
# m_b.stop(stop_action="hold")
# m_c.stop(stop_action="hold")
# print("1 after hold")

print("2 before run")
m_b.run_forever(speed_sp=300)
m_c.run_forever(speed_sp=300)
sleep(2)

print("3 before run")
m_b.run_forever(speed_sp=100)
m_c.run_forever(speed_sp=100)
sleep(2)

m_b.stop(stop_action="hold")
m_c.stop(stop_action="hold")

# m_b = LargeMotor('outB')
# m_c = LargeMotor('outC')
# m_b.run_forever(speed_sp=900)
# m_c.run_forever(speed_sp=-900)
# sleep(5)
# m_b.stop(stop_action="hold")
# m_c.stop(stop_action="hold")
# sleep(5)
