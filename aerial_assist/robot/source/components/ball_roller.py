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
    IN = 1
    OUT = -1

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
            self.ball_roller_motor.Set(IN)
            
        if self.direction == ROLL_FORWARDS:
            self.ball_roller.Set(OUT)
            
        if self.direction == OFF:
            self.ball_roller_motor.Set(0)