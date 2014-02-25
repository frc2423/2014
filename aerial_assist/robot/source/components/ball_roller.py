try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#import modes
from common.modes import *

#Constants
IN = wpilib.Relay.kForward
OUT = wpilib.Relay.kReverse
OFF = wpilib.Relay.kOff
    
#states
AUTO_LOAD = 0
MANUAL = 1

class BallRoller(object):

    '''
        Controls the wheels that roll the ball in and out
        ball_roller_motor         a relay representing the ball rollers motor
         
    '''

    def __init__(self, ball_roller_motor):
        self.ball_roller_motor = ball_roller_motor
        self.direction = OFF
        self.sd = wpilib.SmartDashboard
            
            
    def roll_in(self):
        self.direction = IN
        
    def roll_out(self):
        self.direction = OUT
        
    def off(self):
        self.direction = OFF
        
    def update(self):
        self.ball_roller_motor.Set(self.direction)
            
        self.sd.PutNumber("Ball Roller", self.direction)
        
        self.direction = OFF
        