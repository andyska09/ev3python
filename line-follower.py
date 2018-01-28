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
        print("** this is constructor **")
        print("Read colors from the file: '%s'" % colors_file_name)
        with open('color.txt') as f:
            white = int(f.readline())
            print(white)
            black = int(f.readline())
            print(black)
        self.target = (white - black) / 2 + black
        self.tp = 500
        self.kp = 1.020
        self.ki = 0.049
        self.kd = 5.320
        print("Robot is initialized with values:\n\ttarget = %s\n\tk_d = %s" %
              (self.target, self.kd))

    def write_log(self, log):
        f = open("lightlog.txt","w")
        f.write(log)
        f.close()

    def can_continue(self):
        return (not ts.value()) and ((time.time() - self.t_start) < 10) #or (us.value() > 300))

    def sleduj_caru(self):
        print("\n** this is method.sleduj_caru(s*")
        # on_side = "left"
        on_side = "right"
        integral = 0
        last_err = 0
        max_err = 0
        i = 0

        log = ""
        self.t_start = time.time()
        t1 = datetime.now()
        # Stop program by pressing touch sensor button
        while self.can_continue():
            log_line = "%4d" % i
            if (on_side == "left") and (cl_middle.value() > 80) and (cl_right.value() > 80):
                on_side = "right"
            if (on_side == "right") and (cl_middle.value() > 80) and (cl_left.value() > 80):
                on_side = "left"
            log_line += " %s %3d %3d %3d \n" % (on_side, cl_left.value(), cl_middle.value(), cl_right.value())

            err = self.target - cl_middle.value()
            integral = err + 2/3 * integral
            # This is pid formula
            corr = err * self.kp + integral * \
                self.ki + (err - last_err) * self.kd

            if on_side == "right":
                corr = -corr 

            tp_r = self.tp + (corr * 10) / 2  # this is motor on outB
            tp_l = self.tp - (corr * 10) / 2  # this is motor on outC
            tp_r = min(1000, max(-1000, tp_r))
            tp_l = min(1000, max(-1000, tp_l))
            m_b.run_forever(speed_sp=tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp=tp_l)
            last_err = err
            i = i + 1
            log = log + log_line

        t2 = datetime.now()
        self.write_log(log)

        print(str(t1))
        print(str(t2))
        # print(max_err)

        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")



print("Getting started with objects\n----------------------------\n")
print("1")
lf = LineFollower('color.txt', 1.3, 0, 0)
print("ki = ", lf.ki)
lf.sleduj_caru()