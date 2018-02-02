#!/usr/bin/env python3
# from ev3dev.ev3 import *


from ev3dev.ev3 import *
from time import sleep
from datetime import datetime

cl_left = ColorSensor("in1")  # left cl sensor
cl_middle = ColorSensor("in2")  # middle cl sensor
cl_right = ColorSensor("in3")  # right cl sensor
ts = TouchSensor()
us = UltrasonicSensor()

us.mode = 'US-DIST-CM'
cl_left.mode = 'COL-REFLECT'
cl_middle.mode = 'COL-REFLECT'
cl_right.mode = 'COL-REFLECT'
assert ColorSensor().connected, "Connect a color sensor to any sensor port"
# assert ts.connected, "Connect a touch sensor to any sensor port"
assert us.connected, "Connect a single US sensor to any sensor port"

m_b = LargeMotor('outB')
m_c = LargeMotor('outC')

assert m_b.connected, "Connect the right motor to port b"
assert m_c.connected, "Connect the left motor to port c"

class LineFollower:
    'Program for EV3 to follow a line, implemented using objects.'

    def __init__(self, colors_file_name, kp, ki, kd):
        with open('color.txt') as f:
            self.white = int(f.readline())
            print(self.white)
            self.black = int(f.readline())
            print(self.black)
        self.target = (self.white - self.black) / 2 + self.black
        print("target = %s" % (self.target))

    def write_log(self, log):
        f = open("lightlog.txt","w")
        f.write(log)
        f.close()

    def sleduj_caru(self):
        target = self.target
        tp = 450
        kp = 1.2
        ki = 0.068
        kd = 5.298
        integral = 0
        last_err = 0
        i = 0
        on_side = "L"
        side_was_changed = False 
        log_line = ""
        print("start")
        t_start = time.time()
        # Stop program by pressing touch sensor button
        # (not ts.value()) and
        while (((time.time() - t_start) < 1) or (us.value() > 300)) and i < 1000:
            cmiddle = cl_middle.value()
            if side_was_changed:
                if (cmiddle > 25) and (cmiddle < 75):
                    side_was_changed = False
            else:
                if (on_side == "L"):
                    if (cmiddle > 80) and (cl_right.value() > 80):
                        on_side = "R"
                        side_was_changed = True
                else:
                    if (cmiddle > 80) and (cl_left.value() > 80):
                        on_side = "L"
                        side_was_changed = True
            err = target - cmiddle
            integral = err + ((2/3)*integral)
            # This is pid formula
            corr = (err * kp + integral * ki + (err - last_err) * kd) * 5
            # corr = corr * 5  # (corr * 10) / 2
            if on_side == "R":
                corr = -corr 
            tp_r = tp + corr  # this is motor on outB
            tp_l = tp - corr  # this is motor on outC
            if (tp_r > 1000):
                tp_r = 1000
            if (tp_l > 1000):
                tp_l = 1000    
            # tp_r = min(1000, tp_r)
            # tp_l = min(1000, tp_l)
            m_b.run_forever(speed_sp=tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp=tp_l)
            last_err = err
            # log_line += " %s %s %3d %3d %3d \n" % (on_side, side_was_changed, cleft, cmiddle, cright)
            log_line += "%3d \n" % (cmiddle)
            i += 1 
        print("duration: %s sec" % str(time.time() - t_start))
        self.write_log(log_line)

        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")


lf = LineFollower('color.txt', 1.3, 0, 0)
lf.sleduj_caru()