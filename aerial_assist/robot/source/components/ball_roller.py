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


class BallRoller():

    '''Controls the wheels that roll the ball in/out, hence the name'''

    def __init__(self, ball_roller_motor, ball_roller_sensor):

        self.ball_roller_motor = ball_roller_motor
        self.ball_roller_sensor = ball_roller_sensor
        self.mode = None

    def automatic_mode(self, ball_near, br_forward):

        self.mode = automatic_mode
        self.ball_near = ball_near
        self.br_forward = br_forward

    def manual_spd(self, br_manual_spd):

        self.br_manual_spd = br_manual_spd
        self.mode = manual_spd

    def passing_mode(self, br_backward):
        
        self.br_backward = br_backward
        self.mode = PASSING

    def update(self):

        if self.mode == AUTOMATIC_MODE and self.ball_roller_sensor.Get() <= BALL_NEAR:
            self.ball_roller_motor.Set(br_forward)

        if self.mode == AUTOMATIC_MODE and self.ball_roller_sensor.Get() >= BALL_NEAR:
            self.ball_roller_motor.Set(0)

        if self.mode == MANUAL_SPD:
            self.ball_roller.Set(maunual_spd)

        if self.mode == PASSING:
            self.ball_roller_motor.Set(br_backward)
