try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

    #States
    OFF = 0
    IN = 1
    OUT = 2

    #Constants
    IN = 1
    OUT = -1
    OFF = 0
    
class ball_roller():

    '''
        Controls the wheels that roll the ball in and out
        ball_roller_motor         the motor that controls the wheels that move the ball in and out of the robot
         
    '''

    def __init__(self, ball_roller_motor):
        
        self.ball_roller_motor = ball_roller_motor

    def set(self, direction):
        self.direction = direction

    def update(self):
        self.ball_roller_motor.Set(self.direction)