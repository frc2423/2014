try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

    #States
    automatic_spd = 1
    manual_spd = 2

    #Constants
    '''Place holders for now'''
    BALL_NEAR = 1


class BallRoller():

    '''Controls the wheels that roll the ball in/out, hence the name'''

    def __init__(self, ball_roller_motor, ball_roller_sensor):

        self.ball_roller_motor = ball_roller_motor
        self.ball_roller_sensor = ball_roller_sensor
        self.mode = None

    def automatic_spd(self, ball_near, br_forward):

        self.mode = automatic_spd

    def manual_spd(self, br_manual_spd):
        
        self.mode = manual_spd

    def update(self):

        if self.mode == automatic_spd and self.ball_roller_sensor.Get() <= BALL_NEAR:
            self.ball_roller_motor.Set(br_forward)

        if self.mode == automatic_spd and self.ball_roller_sensor.Get() >= BALL_NEAR:
            self.ball_roller_motor.Set(0)

        if self.mode == manual_spd:
            self.ball_roller.Set(maunual_spd)
