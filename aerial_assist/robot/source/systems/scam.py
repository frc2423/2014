''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#scam motor controls the linear actuator

#Modes
ANGLE_CONTROL = 0
LOADING = 1
PASSING = 2

#Variables
'''place holders for now'''
ball_near = .5
br_forward = 1
loading_spd = 1
br_backward = -1
scam_backward = -1
    
class scam(object):
    
    def __init__(self, scam_motor, scam_pot, igus_slide, ball_roller):
        self.scam_motor = scam_motor    
        self.scam_pot = scam_pot
        self.igus_slide = igus_slide
        self.ball_roller = ball_roller
        self.mode = None

    def angle_control(self, scam_angle):
        self.scam_angle = scam_angle

        self.mode = ANGLE_CONTROL

    def load_ball(self, loading_angle, loading_spd):
        self.Loading_angle = loading_angle
    #loadimg angle and spd might never change but I'm not sure
        self.mode = LOADING

    def pass_ball(self, passing_angle)

        self.passing_angle = passing_angle
        self.mode = PASSING

    def update(self):

        if self.mode == ANGLE_CONTROL:
            self.scam_motor.Set(self.scam_angle)

        if self.mode == LOADING and self.scam_pot.Get() != self.loading_angle:
            self.ball_roller.automatic_mode(ball_near, br_forward)
            self.scam_motor.Set(loading_spd)
#might squish the ball writtent this way

        if self.mode == LOADING and self.scam_pot.Get() == self.loading_angle:
            self.ball_roller.automatic_mode(ball_near, br_forward)
            self.scam_motor.Set(0)

        if self.mode == PASSING and self.scam_pot.Get() == self.assing_angle:
            self.ball_roller.passing_mode(br_backward)
            self.scam_motor.Set(0)

        if self.mode == PASSING and self.scam_pot.Get() != self.assing_angle:
            self.ball_roller.passing_mode(br_backward)
            self.scam_motor.Set(scam_backwards)
            
