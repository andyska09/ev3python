#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

clL = ColorSensor("in1") #left cl sensor
clM = ColorSensor("in2") #middle cl sensor
clR = ColorSensor("in3") #right cl sensor
ts = TouchSensor()

clL.mode = 'COL-REFLECT'
clM.mode = 'COL-REFLECT'
clR.mode = 'COL-REFLECT'
assert ColorSensor().connected, "Connect a color sensor to any sensor port"
assert ts.connected, "Connect a touch sensor to any sensor port"


m_b = LargeMotor('outB')
m_c = LargeMotor('outC')


class LineFollower:
    'Program for EV3 to follow a line, implemented using objects.'

    def __init__(self, colors_file_name, kp, ki, kd):
        print("** this is constructor **")
        print("Read colors from the file: '%s'" % colors_file_name)
        with open('color.txt') as f:
            white = int(f.readline())
            print(white)
            black = int(f.readline())
            print(black)
        self.target = (white - black) / 2
        self.tp = 300
        self.kp = kp
        self.ki = ki
        self.kd = kd
        print("Robot is initialized with values:\n\ttarget = %s\n\tk_d = %s" %
              (self.target, self.kd))

    def sleduj_caru(self):
        print("\n** this is method.sleduj_caru(s*")
        integral = 0
        last_err = 0
        while not ts.value():    # Stop program by pressing touch sensor button
            print(clM.value())
            err = self.target - clM.value()
            integral = err + integral
            #This is pid formula
            corr = err * self.kp + integral * self.ki + (err - last_err) * self.kd
            tp_r = self.tp + (corr * 10)/2         #this is motor on outB
            tp_l = self.tp - (corr * 10)/2        #this is motor on outC
            m_b.run_forever(speed_sp= tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp= tp_l)
            last_err = err
        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")


print("Getting started with objects\n----------------------------\n")
print("1")
lf = LineFollower('color.txt', 1, 0, 0)
print("2")

lf.sleduj_caru()
