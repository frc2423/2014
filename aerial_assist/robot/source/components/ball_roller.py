try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

    #States
    AUTOMATIC_MODE = 1
    MAUNUAL_SPD = 2
    PASSING = 0

    #Constants
    '''Place holders for now'''
    BALL_NEAR = 1
    FORWARD_ROLL_SPEED = 1
    BACKWARD_ROLL_SPEED = -1

class BallRoller():

    '''
        Controls the wheels that roll the ball in and out
        ball_roller_motor         the motor that controls the wheels that move the ball in and out of the robot
        ball_rollor_sensor        used to detect whether or not there is a ball in front of the robot
         
    '''

    def __init__(self, ball_roller_motor, ball_roller_sensor):
        
        self.ball_roller_motor = ball_roller_motor
        self.ball_roller_sensor = ball_roller_sensor
        self.mode = None

    def automatic_mode(self):
        self.mode = AUTOMATIC_MODE

    def roll_forwards(self):

        self.manual_roll_speed = manual_roll_speed
        self.mode = ROLL_FORWARDS
        
    def roll_backwards(self):
        
        self.mode = ROLL_BACKWARDS

        
    def check_for_ball
        if self.ball_roll_sensor <= BALL_NEAR_DISTANCE:
            return True
        else:
            return False

    def update(self):

        if self.mode == AUTOMATIC_MODE and check_for_ball == True:
            self.ball_roller_motor.Set(FORWARD_ROLL_SPEED)

        if self.mode == AUTOMATIC_MODE and self.check_for_ball == False:
            self.ball_roller_motor.Set(0)

        if self.mode == ROLL_BACKWARDS:
            self.ball_roller_motor.Set(BACKWARD_ROLL_SPEED)