try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#Constants
IN = wpilib.Relay.kForward
OUT = wpilib.Relay.kReverse
OFF = wpilib.Relay.kOff
    
class BallRoller(object):

    '''
        Controls the wheels that roll the ball in and out
        ball_roller_motor         a relay representing the ball rollers motor
         
    '''

    def __init__(self, ball_roller_motor):
        self.ball_roller_motor = ball_roller_motor

    def set(self, direction):
        self.direction = direction

    def update(self):
        self.ball_roller_motor.Set(self.direction)