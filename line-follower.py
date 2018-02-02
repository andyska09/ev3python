#!/usr/bin/env python3
# from ev3dev.ev3 import *


from ev3dev.ev3 import *
from time import sleep
from datetime import datetime

cl_left = ColorSensor("in1")  # left cl sensor
cl_middle = ColorSensor("in2")  # middle cl sensor
cl_right = ColorSensor("in3")  # right cl sensor
ts = TouchSensor()
# us = UltrasonicSensor()

# us.mode = 'US-DIST-CM'
cl_left.mode = 'COL-REFLECT'
cl_middle.mode = 'COL-REFLECT'
#cl_right.mode = 'COL-REFLECT'
assert ColorSensor().connected, "Connect a color sensor to any sensor port"
# assert ts.connected, "Connect a touch sensor to any sensor port"
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
        self.kp = 1.2
        self.ki = 0.068
        self.kd = 5.298
        print("target = %s" % (self.target))

    def sleduj_caru(self):
        integral = 0
        last_err = 0
        i = 0
        self.t_start = time.time()
        print("start")
        # Stop program by pressing touch sensor button
        while (not ts.value()):
            # (((time.time() - t_start) < 10) or (us.value() > 300)):
            # print(i)
            # print(cl_middle.value())
            err = self.target - cl_middle.value()
            integral = err + ((2/3)*integral)
            # This is pid formula
            corr = err * self.kp + integral * \
                self.ki + (err - last_err) * self.kd
            tp_r = self.tp + (corr * 10) / 2  # this is motor on outB
            tp_l = self.tp - (corr * 10) / 2  # this is motor on outC
            tp_r = min(1000, max(-1000, tp_r))
            tp_l = min(1000, max(-1000, tp_l))
            m_b.run_forever(speed_sp=tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp=tp_l)
            last_err = err
        print("duration: %s sec" % str(time.time() - self.t_start))


        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")


lf = LineFollower('color.txt', 1.3, 0, 0)
lf.sleduj_caru()