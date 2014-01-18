try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

class BallRoller():

    def __init__(self, ball_roller_motor, ball_roller_sensor):

        self.ball_roller_motor = ball_roller_motor
        self.ball_roller_sensor = ball_roller_sensor

    def automatic_spd(self, ball_near, br_forward):

        if ball_roller_sensor.Get() <= ball_near:
            self.ball_roller_motor.Set(br_forward)
        else self.ball_roller_motor.Set(0)

    def manual_spd(self, br_manual_spd):
        ball_roller.motor.Set(br_maunual_spd)

    def update(self):

        #needs to check if the ball is there
