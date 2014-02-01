try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

    #States
    OFF = 0
    ROLL_FORWARDS = 1
    ROLL_BACKWARDS = 2

    #Constants
    '''Place holders for now'''
    FORWARD_ROLL_SPEED = 1
    BACKWARD_ROLL_SPEED = -1

class ball_roller():

    '''
        Controls the wheels that roll the ball in and out
        ball_roller_motor         the motor that controls the wheels that move the ball in and out of the robot
        ball_rollor_sensor        used to detect whether or not there is a ball in front of the robot
         
    '''

    def __init__(self, ball_roller_motor, ball_roller_sensor):
        
        self.ball_roller_motor = ball_roller_motor
        self.ball_roller_sensor = ball_roller_sensor

    def set(self, direction):
        self.direction = direction

    def update(self):

        if self.direction == ROLL_BACKWARDS:
            self.ball_roller_motor.Set(BACKWARD_ROLL_SPEED)
            
        if self.direction == ROLL_FORWARDS:
            self.ball_roller.Set(FORWARD_ROLL_SPEED)
            
        if self.direction == OFF:
            self.ball_roller_motor.Set(0)