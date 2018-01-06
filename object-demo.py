#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
from datetime import datetime

cl_left = ColorSensor("in1") #left cl sensor
cl_middle = ColorSensor("in2") #middle cl sensor
cl_right = ColorSensor("in3") #right cl sensor
ts = TouchSensor()

cl_left.mode = 'COL-REFLECT'
cl_middle.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'
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
        self.tp = 250
        self.kp = kp
        self.ki = ki
        self.kd = kd
        print("Robot is initialized with values:\n\ttarget = %s\n\tk_d = %s" %
              (self.target, self.kd))

    def sleduj_caru(self):
        print("\n** this is method.sleduj_caru(s*")
        integral = 0
        last_err = 0
        i = 0
        t1 = datetime.now()
        while (not ts.value()) and i < 680:    # Stop program by pressing touch sensor button
            # print(i)
            # print(cl_middle.value())
            err = self.target - cl_middle.value()
            integral = err + integral
            #This is pid formula
            corr = err * self.kp + integral * self.ki + (err - last_err) * self.kd
            tp_r = self.tp + (corr * 10)/2         #this is motor on outB
            tp_l = self.tp - (corr * 10)/2        #this is motor on outC
            m_b.run_forever(speed_sp= tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp= tp_l)
            last_err = err
            i = i + 1
        t2 = datetime.now()
        print(str(t1))
        print(str(t2))

        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")


print("Getting started with objects\n----------------------------\n")
print("1")
lf = LineFollower('color.txt', 1.3, 0, 0)
print("ki = ",lf.ki)

lf.sleduj_caru()
