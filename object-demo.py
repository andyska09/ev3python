#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *

assert cl.connected, "Connect a color sensor to any sensor port"
assert ts.connected, "Connect a touch sensor to any sensor port"

cl = ColorSensor()
ts = TouchSensor()
cl.mode = 'COL-REFLECT'

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
        self.tp = 500
        self.kp = kp
        self.ki = ki
        self.kd = kd
        print("Robot is initialized with values:\n\ttarget = %s\n\tk_d = %s" %(self.target, self.kd))

    def sleduj_caru(self):
        print("\n** this is method.sleduj_caru(s*")
        print("Start the line following using:")
        print("\ttarget = %s" % self.target)
        print("\tk_d = %s" % self.kd)
        integral = 0
        last_err = 0
        while not ts.value():    # Stop program by pressing touch sensor button
            err = self.target - cl.value()
            integral = err + integral
            
            #This is pid formula
            corr = ((self.target - cl.value())*self.kp) + ((integral*self.ki) + ((err - last_err)*self.kd )
            
            b = tp + corr*10
            m_b.run_forever(speed_sp = b)          #This will makes robot turning
            m_c.run_forever(speed_sp = tp)
            
            last_err = err
            
        m_b.stop(stop_action="hold")
        m_c.stop(stop_action="hold")

print("Getting started with objects\n----------------------------\n")
print("1")
lf = LineFollower('color.txt', 1, 0, 0)
print("2")

lf.sleduj_caru()
