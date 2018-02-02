#!/usr/bin/env python3
# from ev3dev.ev3 import *


from ev3dev.ev3 import *
from time import sleep
import time
from datetime import datetime

cl_left = ColorSensor("in1")  # left cl sensor
cl_middle = ColorSensor("in2")  # middle cl sensor
cl_right = ColorSensor("in3")  # right cl sensor
ts = TouchSensor()
us = UltrasonicSensor()

# us.mode = 'US-DIST-CM'
cl_left.mode = 'COL-REFLECT'
cl_middle.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'
assert ColorSensor().connected, "Connect a color sensor to any sensor port"
assert ts.connected, "Connect a touch sensor to any sensor port"
# assert us.connected, "Connect a single US sensor to any sensor port"

m_b = LargeMotor('outB')
m_c = LargeMotor('outC')

assert m_b.connected, "Connect the right motor to port b"
assert m_c.connected, "Connect the left motor to port c"

class LineFollower:
    'Program for EV3 to follow a line, implemented using objects.'

    def __init__(self, colors_file_name, kp, ki, kd):
        with open('color.txt') as f:
            white = int(f.readline())
            print(white)
            black = int(f.readline())
            print(black)
        self.target = (white - black) / 2 + black
        self.tp = 450
        self.kp = 1.020
        self.ki = 0.037
        self.kd = 7.108
        print("Robot is initialized with values:\n\ttarget = %s\n\tk_d = %s" %
              (self.target, self.kd))

    def write_log(self, log):
        f = open("lightlog.txt","w")
        f.write(log)
        f.close()

    def sleduj_caru(self):
        print("\n** this is method.sleduj_caru(s*")
        on_side = "left"
        integral = 0
        last_err = 0
        i = 0
        side_was_changed = False 

        log = ""
        self.t_start = time.time()
        # Stop program by pressing touch sensor button
        while (not ts.value()) and i < 800: #((time.time() - self.t_start) < 10) #or (us.value() > 300)):
            # log_line = "%4d" % i
            cleft = cl_left.value()
            cmiddle = cl_middle.value()
            cright = cl_right.value()
            # if side_was_changed:
            #     if (cmiddle > 25) and (cmiddle < 75):
            #         side_was_changed = False
            # else:
            #     if (on_side == "left"):
            #         if (cmiddle > 80) and (cright > 80):
            #             on_side = "right"
            #             side_was_changed = True
            #     else:
            #         if (cmiddle > 80) and (cleft > 80):
            #             on_side = "left"
            #             side_was_changed = True
    
            # log_line += " %s %s %3d %3d %3d \n" % (on_side, side_was_changed, cleft, cmiddle, cright)

            err = self.target - cmiddle
            integral = err + integral
            # This is pid formula
            corr = err * self.kp + integral * \
                self.ki + (err - last_err) * self.kd

            # if on_side == "right":
                # corr = -corr 

            tp_r = self.tp + (corr * 10) / 2  # this is motor on outB
            tp_l = self.tp - (corr * 10) / 2  # this is motor on outC
            tp_r = min(1000, max(-1000, tp_r))
            tp_l = min(1000, max(-1000, tp_l))
            m_b.run_forever(speed_sp=tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp=tp_l)
            last_err = err
            i = i + 1
            # log = log + log_line
        log_line = "duration: %s sec" % str(time.time() - self.t_start)
        log += log_line
        self.write_log(log)
        print(log_line)
        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")



print("Getting started with objects\n----------------------------\n")
print("1")
lf = LineFollower('color.txt', 1.3, 0, 0)
print("ki = ", lf.ki)
lf.sleduj_caru()