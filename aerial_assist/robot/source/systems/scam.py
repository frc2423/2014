''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#scam motor controls the linear actuator

#Modes
SHOOT_MODE = 0
SET_SHOOT_MODE = 1
LOAD_MODE = 2
SET_LOAD_MODE = 3
SET_PASS_MODE = 4
PASS_MODE = 5
PASSED = 6

#Variables 
'''place holders for now'''
ANGLE_SPEED = 1
LOADING_ANGLE = 0
SHOOTING_ANGLE = 1
PASSING_ANGLE = 0
HAS_PASSED_TIME = 1

#positions for scam angle
LOADING = 0 #todo: put actual value here, float I think between 0 - 1
SHOOTING = 1 #todo: put actual value here, float I think between 0 - 1
PASSING = 0 #todo: put actual value here, float I think between 0 - 1
class scam(object):
    
    def __init__(self, l_actuator, igus_slide, ball_roller, ls_loading):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           
           os_rear            to stop the slide when it is all the way retracted
           ls_loading         used to know when the slide is all the way down
           l_actuator         linear actuator controls the 4 bar linkage - has a potentiometer attached to it
           igus_slide         instance of the igus_slide, controls the winch
           ball_roller        instance of the ball_roller, moves the balls on and off the slide
           
           values used to set real positions of the Scam
           
           l_actuator_val     value to set the l_actuator position, maybe speed or position
        '''
        self.ls_loading = ls_loading
        self.l_actuator = l_actuator    
        #self.l_actuator_pot = scam_pot -  pot connected straight to the jag
        self.igus_slide = igus_slide
        self.ball_roller = ball_roller
        self.mode = None
        self.l_actuator_val = None
        self.has_passed_timer = wpilib.Timer
        
    def set_scam(self, val):
        '''
            function: sets l_actuator_val to the desired position
            
            variable: val - maybe desired position or desired speed of the l_actuator 
        '''
        self.l_actuator_val = val
    
    def pass_mode(self):
        if not self.mode == SET_PASS_MODE:
            self.igus_slide.has_shot_timer.Stop()
            self.igus_slide.has_shot_timer.Reset()
            self.igus_slide.has_ball_timer.Stop()
            self.igus_slide.has_ball_timer.Reset()
            self.igus_slide.retract()
            self.ball_roller.set(self.ball_roller.OUT)
            self.set_scam(PASSING_ANGLE)
            self.mode = SET_PASS_MODE
            
    def load_mode(self):
        if not self.mode == SET_LOAD_MODE:
            self.has_passed_timer.Stop()
            self.has_passed_timer.Reset()
            self.igus_slide.has_shot_timer.Stop()
            self.igus_slide.has_shot_timer.Reset()
            self.igus_slide.retract()
            self.ball_roller.set(self.ball_roller.OFF)
            self.set_scam(LOADING_ANGLE)
            self.mode = SET_LOAD_MODE
        
    def shoot_mode(self):
        if not self.SET_SHOOT_MODE:
            self.has_passed_timer.Stop()
            self.has_passed_timer.Reset()
            self.igus_slide.has_ball_timer.Stop()
            self.igus_slide.has_ball_timer.Reset()
            self.igus_slide.retract()
            self.set_scam(SHOOTING_ANGLE)
            self.ball_roller.set(self.ball_roller.OFF)
            self.mode = SET_SHOOT_MODE
            
    def scam_in_postion(self, position):
        '''
            Compares current scam position to the expected position
        '''
        if self.l_actuator.GetPosition() == position:
            return True
        else:
            return True
        
        '''       
            Look at the diffrence of this code and your originals
        
            if self.position == "LOADING":
                if self.scam_angle == LOADING_ANGLE:
                    return True
                else:
                    return False
                
            if self.position =="SHOOTING":
                if self.scam_anlge == SHOOTING_ANGLE:
                    return True
                else:
                    return False
        '''
    def update(self):
        
        if self.mode == SET_PASS_MODE:
            if self.scam_in_position(PASSING):
                self.mode = PASS_MODE
        
        if self.mode == PASS_MODE:
            
            if self.has_passed_timer.Get == 0:
                self.has_passed_timer.Start()
                
            elif self.has_passed_timer >= HAS_PASSED_TIME:
                self.mode = PASSED
                self.has_passed_timer.Stop()
                self.has_passed_timer.Reset()
                self.ball_roller.set(self.ball_roller.OFF)
            
        #code that deals with shooting and shooting transition states
        if self.mode == SET_SHOOT_MODE:
            
            if self.l_actuator.GetPosition() < SHOOTING_ANGLE:
                self.ball_roller.set(self.ball_roller.IN)
                
            if self.scam_in_postion(SHOOTING):
                self.mode = SHOOT_MODE
                
        if self.mode == SHOOT_MODE:
            self.ball_roller.set(self.ball_roller.OFF)
            
        
        #code that deals with loading and loading transition states
        
        if self.mode == SET_LOAD_MODE:
            if self.ls_loading.Get() or self.scam_in_position(LOADING):
                self.mode = LOAD_MODE
        
        if self.mode == LOAD_MODE:
            if self.auto_load and self.igus_slide.has_ball():
                self.shoot_mode()
            
            else:
                self.ball_roller.set(self.ball_roller.OUT)
                
        self.l_actuator.Set(self.angle)
        
        #update all our components here need updated
        self.l_actuator.update()
        self.ball_roller.update()
        self.igus_slide.update()
        
        