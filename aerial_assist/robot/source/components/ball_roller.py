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

    def __init__(self, ball_roller_motor, auto_mode = AUTO):
        self.ball_roller_motor = ball_roller_motor
        self.auto_mode = auto_mode
        self.direction = OFF
        self.mode = MANUAL
    def set_mode(self, mode):
        '''
            sets the expected action in the given mode
        '''
        if self.mode == LOAD_MODE and self.auto_mode:
            self.mode = AUTO_LOAD
            self.direction = IN
        else:
            self.mode = MANUAL
            self.direction = OFF
            
    def set(self, direction):
        '''
            if we use set we are again running the balls manually 
        '''
        self.direction = direction
        self.mode = MANUAL

    def update(self):
        print(self.direction)
        self.ball_roller_motor.Set(self.direction)
        
        #reset the speed if we are not in auto mode
        if not self.mode == AUTO_LOAD:
            self.direction = 0