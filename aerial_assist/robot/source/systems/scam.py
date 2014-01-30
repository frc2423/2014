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
        #d_angle? No clue what that is.
        #Angle control mode for up but limit switch mode for loading mode (down).
        self.d_angle = d_angle
        self.mode = ANGLE_CONTROL
        
    def load_ball(self):
        if self.igus_slide.ready_to_load == True and self.ball_roller.check_for_ball == True:
            self.mode = LOADING    
            
    #Check the igus_slide for other comments    
        
    def pull_winch(self):
        pass
    
    def update(self):
        
        #Not really sure what you're are trying to do. Need limit switch control for going down.
        if self.mode == ANGLE_CONTROL and self.scam_pot.Get() > self.d_angle + ANGLE_THRESHOLD:
            self.scam_motor.Set(ANGLE_SPEED)
        
        if self.mode == ANGLE_CONTROL and self.scam_pot.Get() < self.d_angle - ANGLE_THRESHOLD:
            self.scam_motor.Set(ANGLE_SPEED * -1)
#This seemed OK
        if self.mode == LOADING and self.scam_pot.Get() != LOADING_ANGLE:
            self.angle_control(LOADING_ANGLE)
            
        if self.mode == LOADING and self.scam_pot.Get() == self.loading_angle:
            self.ball_roller.automatic_mode()
            self.scam_motor.Set(0)
