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
btn = Button()

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
        tp = 500
        kp = 11.363
        ki = 0
        kd = 0
        integral = 0
        last_err = 0
        i = 0
        prev_sign = None
        oscil_count = 0
        on_side = "L"
        side_was_changed = False 
        log_line = ""
        print("start")
        t_start = time.time()
        # Stop program by pressing touch sensor button
        # (not ts.value()) and
        # 
        # while ( \
        #     and ((i % 11 != 0) or (not btn.backspace)):        
        while (i % 11 != 0) or \
            (not btn.backspace and \
            ((time.time() - t_start) < 80) or (us.value() > 300)) and i < 1000:
            cright = 0
            cmiddle = cl_middle.value()
            cleft = 0
            
            # if side_was_changed:
            #     if (cmiddle > 25) and (cmiddle < 75):
            #         side_was_changed = False
            # else:
            #     if (on_side == "L"):
            #         if (cmiddle > 80):
            #             cright = cl_right.value()
            #             if  (cright > 80):
            #                 on_side = "R"
            #                 side_was_changed = True
            #     else:
            #         if (cmiddle > 80):
            #             cleft = cl_left.value()
            #             if (cleft > 80):
            #                 on_side = "L"
            #                 side_was_changed = True
            err = target - cmiddle
            integral = err + ((2/3)*integral)
            # This is pid formula
            corr = (err * kp + integral * ki + (err - last_err) * kd) / 2
            # corr = corr * 5  # (corr * 10) / 2
            if on_side == "R":
                corr = -corr 
            tp_r = tp + corr  # this is motor on outB
            tp_l = tp - corr  # this is motor on outC
            if (tp_r > 1000):
                tp_r = 1000
            elif (tp_r < -1000):
                tp_r = -1000
            if (tp_l > 1000):
                tp_l = 1000    
            elif (tp_l < -1000):
                tp_l = -1000
            m_b.run_forever(speed_sp=tp_r)  # This will makes robot turning
            m_c.run_forever(speed_sp=tp_l)
            last_err = err
            if prev_sign is None:
                if err > 0:
                    prev_sign = 1
                else:
                    prev_sign = -1
            else:
                if prev_sign == 1 and err < 0:
                    oscil_count += 1
                elif prev_sign == -1 and err > 0:
                    oscil_count += 1 
                if err > 0:
                    prev_sign = 1
                else:
                    prev_sign = -1                   
            log_line += " %s %s %3d %3d \n" % (str(prev_sign), err> 0, oscil_count, err)
            # log_line += " %s %s %3d %3d %3d \n" % (on_side, side_was_changed, cleft, cmiddle, cright)
            i += 1 
        print("duration: %s sec" % str(time.time() - t_start))
        self.write_log(log_line)

        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")


lf = LineFollower('color.txt', 1.3, 0, 0)
lf.sleduj_caru()