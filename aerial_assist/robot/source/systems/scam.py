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
ANGLE_SPEED = 1
LOADING_ANGLE = 0
ANGLE_THRESHOLD = .5
class scam(object):
    
    def __init__(self, scam_motor, scam_pot, igus_slide, ball_roller):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           scam_motor        the motor attached to the linear actuator, controls 4 bar linkage
           scam_pot          detects what angle the igus_slide is at
        '''
        
        self.scam_motor = scam_motor    
        self.scam_pot = scam_pot
        self.igus_slide = igus_slide
        self.ball_roller = ball_roller
        self.mode = None

    def angle_control(self, d_angle):
        self.d_angle = d_angle
        self.mode = ANGLE_CONTROL
        
    def load_ball():
        if self.igus_slide.ready_to_load == True and self.ball_roller.check_for_ball == True:
            self.mode == LOADING

    def pass_ball(self):
        self.igus_slide.slow_release()
        
        
        
    def pull_winch(self):
        

    def update(self):

        if self.mode == ANGLE_CONTROL and self.scam_pot.Get() > d_angle + ANGLE_THRESHOLD:
            self.scam_motor.Set(angle_speed)
        
        if self.mode == ANGLE_CONTROL and self.scam_pot.Get() < d_angnle - ANGLE_THRESHOLD:
            self.scam_motor.Set(angle_speed * -1)

        if self.mode == LOADING and self.scam_pot.Get() != LOADING_ANGLE:
            self.angle_control(LOADING_ANGLE)
            
#might squish the ball writtent this way

        if self.mode == LOADING and self.scam_pot.Get() == self.loading_angle:
            self.ball_roller.automatic_mode()
            self.scam_motor.Set(0)

        if self.mode == PASSING and self.scam_pot.Get() == self.passing_angle:
            
        if self.mode == PASSING and self.scam_pot.Get() != self.passing_angle:
            self.ball_roller.passing_mode(br_backward)
            self.scam_motor.Set(scam_backwards)
            
