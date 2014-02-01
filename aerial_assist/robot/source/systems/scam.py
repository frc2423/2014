''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#scam motor controls the linear actuator

#Modes
ANGLE_CONTROL = 0
PASSING = 1
LOAD_MODE = 2
SET_LOAD_MODE = 3

#Variables 
'''place holders for now'''
ANGLE_SPEED = 1
LOADING_ANGLE = 0
ANGLE_THRESHOLD = .5

class scam(object):
    
    def __init__(self, l_actuator, scam_pot, igus_slide, ball_roller, ls_loading):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           
           os_rear            to stop the slide when it is all the way retracted
           ls_loading         used to know when the slide is all the way down
           l_actuator         linear actuator controls the 4 bar linkage
           l_actuator_pot     used to tell what angle the slide is at
           igus_slide         instance of the igus_slide, controls the winch
           ball_roller        instance of the ball_roller, moves the balls on and off the slide
        '''
        self.ls_loading = ls_loading
        self.l_actuator = l_actuator    
        self.l_actuator_pot = scam_pot
        self.igus_slide = igus_slide
        self.ball_roller = ball_roller
        self.mode = None
        self.l_actuator_val = None
        
    def set_scam_angle(self, angle):
        '''
            figures out what position the actuator should be in so the slide is at that specific angle 
        '''
        self.l_actuator_val = angle
    
    def set_scam_speed(self, speed):
        '''
            sets the speed of the linear actuator motor
        '''
        self.l_actuator_val = speed
        
    def load_mode(self):
        if not self.mode == SET_LOAD_MODE:
            self.igus_slide.retract()
            self.ball_roller.set(self.ball_roller.OFF)
            self.set_scam_angle(LOADING_ANGLE)
            
            self.mode = SET_LOAD_MODE
        
    def scam_in_postion(self, position):
        position = self.position
        if self.position == "LOADING":
            if self.scam_angle == LOADING_ANGLE:
                return True
            else:
                return False
    
    def update(self):
        
        if self.mode == SET_LOAD_MODE:
            if self.ls_loading.Get() or self.scam_in_position("LOADING"):
                self.mode = LOAD_MODE
        
        if self.mode == LOAD_MODE:
            if self.auto_load and self.igus_slide.has_ball():
                self.shoot_mode
            
            else:
                self.ball_roller.set("ON")
                
        self.l_actuator.Set(self.angle)