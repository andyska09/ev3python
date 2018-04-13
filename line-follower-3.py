#!/usr/bin/env python3
# from ev3dev.ev3 import *


from ev3dev.ev3 import *
from time import sleep
from datetime import datetime
import traceback

cl_left = ColorSensor("in1")  # left cl sensor
cl_middle = ColorSensor("in2")  # middle cl sensor
cl_right = ColorSensor("in3")  # right cl sensor
ts = TouchSensor()
us = UltrasonicSensor()
btn = Button()

us.mode = 'US-DIST-CM'
cl_left.mode = 'COL-REFLECT'
cl_middle.mode = 'COL-REFLECT'
# cl_right.mode = 'COL-REFLECT'
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
        self.start_with_us_after_sec = 60  # to be adjusted manually
        self.i_duration_ms = 11.4 # to be adjusted manually
        self.start_with_us_after_i = self.start_with_us_after_sec * 1000 / self.i_duration_ms
        print("target = %s" % (self.target))

    def write_log(self, log):
        f = open("lightlog.txt","w")
        f.write(log)
        f.close()

    def sleduj_caru(self):
        target = self.target
        # kp = 6.818
        # ki = 0.347
        # kd = 33.461
        tp = 450
        kp = 12.516
        ki = 0.279
        kd = 55.212
        integral = 0
        last_err = 0
        i = 0
        on_side = "L"
        side_was_changed = False 
        log_line = ""
        print("start")
        t_start = time.time()
        while ((i % 11 != 0) or (not btn.backspace)) \
            and ((i < self.start_with_us_after_i) or  (i % 78 != 0) or (us.value() > 350)):
            cright = 0
            cmiddle = cl_middle.value()
            cleft = 0
            # if side_was_changed:
            #     if (cmiddle > 25) and (cmiddle < 75):
            #         side_was_changed = False
            # else:
            #     if (on_side == "L"):
            #         if (cmiddle > 90):
            #             cright = cl_right.value()
            #             if  (cright > 90):
            #                 on_side = "R"
            #                 side_was_changed = True
            #     else:
            #         if (cmiddle > 90):
            #             cleft = cl_left.value()
            #             if (cleft > 90):
            #                 on_side = "L"
            #                 side_was_changed = True
            err = target - cmiddle
            integral = err + ((2/3)*integral)
            # This is pid formula
            corr_p = (err * kp)
            corr_i = (integral * ki)
            corr_d = ((err - last_err) * kd)
            corr = (corr_p + corr_i + corr_d) / 2
            if on_side == "R":
                corr = -corr 
            tp_r = tp + corr  # this is motor on outB
            tp_l = tp - corr  # this is motor on outC
            tp_rc = tp_r
            tp_lc = tp_l
            cut_r = 0
            cut_l = 0
            if (tp_l > 1000):
                cut_l = tp_l - 1000
                # tp_l = 1000   
                tp_lc = 1000   
                tp_rc = tp_r - cut_l
                tp_rc = min(1000, max(-1000, tp_rc))   
                Leds.set_color(Leds.LEFT, Leds.RED)   
                log_line += "L1 %4d %3d %4d %4d \n" % (i, cut_l, tp_lc, tp_rc)                     
            elif (tp_l < -1000):
                cut_l = tp_l + 1000 
                # tp_l = -1000
                tp_lc = -1000
                tp_rc = tp_r - cut_l
                tp_rc = min(1000, max(-1000, tp_rc))
                log_line += "L2 %4d %3d %4d %4d \n" % (i, cut_l, tp_lc, tp_rc)                     
            if (tp_r > 1000):
                cut_r = tp_r - 1000
                # tp_r = 1000
                tp_rc = 1000
                tp_lc = tp_l - cut_r
                tp_lc = min(1000, max(-1000, tp_lc)) 
                Leds.set_color(Leds.RIGHT, Leds.RED)               
                log_line += "R1 %4d %3d %4d %4d \n" % (i, cut_r, tp_lc, tp_rc)                     
            elif (tp_r < -1000):
                cut_r = tp_r + 1000 
                # tp_r = -1000
                tp_rc = -1000
                tp_lc = tp_l - cut_r
                tp_lc = min(1000, max(-1000, tp_lc))
                log_line += "R2 %4d %3d %4d %4d \n" % (i, cut_r, tp_lc, tp_rc)                     
            m_b.run_forever(speed_sp=tp_rc)  # This will makes robot turning
            m_c.run_forever(speed_sp=tp_lc)
            last_err = err
            #  log_line += " %s %s %3d %3d %3d \n" % (on_side, side_was_changed, cleft, cmiddle, cright)
            # if (cut_r != 0) or (cut_l != 0):
                # log_line += " %3d % 5.3f % 5.3f % 5.3f % 5.3f % 5.3f % 5.3f\n" % (
            # i, tp_l,  tp_r, tp_lc, tp_rc, cut_l, cut_r)
            i += 1 
        print("duration: %s sec" % str(time.time() - t_start))
        self.write_log(log_line)

        m_b.stop(stop_action="brake")
        m_c.stop(stop_action="brake")

# Leds.set_color(Leds.RIGHT, Leds.GREEN)
# Leds.set_color(Leds.LEFT, Leds.GREEN)
try:
    lf = LineFollower('color.txt', 1.3, 0, 0)
    lf.sleduj_caru()
except:
    print('neco je spatne')
    traceback.print_exc()
    print('stop motors')
    m_b.stop(stop_action="brake")
    m_c.stop(stop_action="brake")
finally:
    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    Leds.set_color(Leds.LEFT, Leds.GREEN)