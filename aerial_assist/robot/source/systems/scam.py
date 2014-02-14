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
'''approx value not tested'''
PROPORTION_VALUE = 7.5

OFFSET = 1
#positions for scam angle
LOADING = 0 #todo: put actual value here, float I think between 0 - 1
SHOOTING = 1 #todo: put actual value here, float I think between 0 - 1
PASSING = 0 #todo: put actual value here, float I think between 0 - 1
class Scam(object):
    
    def __init__(self, l_actuator, igus_slide, ball_roller):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           
           l_actuator         linear actuator controls the 4 bar linkage - has a potentiometer attached to it
           igus_slide         instance of the igus_slide, controls the winch
           ball_roller        instance of the ball_roller, moves the balls on and off the slide
           
           values used to set real positions of the Scam
           
           l_actuator_val     value to set the l_actuator position, maybe speed or position
        '''
        self.l_actuator = l_actuator    
        #self.l_actuator_pot = scam_pot -  pot connected straight to the jag
        self.igus_slide = igus_slide
        self.ball_roller = ball_roller
        self.mode = None
        self.l_actuator_val = None
        self.has_passed_timer = wpilib.Timer
        
    def get_mode(self):
        return self.mode    
    
    def clear_timers(self):
        self.igus_slide.has_shot_timer.Stop()
        self.igus_slide.has_shot_timer.Reset()
        self.igus_slide.has_ball_timer.Stop()
        self.igus_slide.has_ball_timer.Reset()
    
    def pass_mode(self):
        if not self.mode == SET_PASS_MODE:
            self.clear_timers()
            #igus slide position is not important to us here
            self.ball_roller.set(self.ball_roller.OUT)
            self.set_scam(PASSING_ANGLE)
            self.mode = SET_PASS_MODE
            
    def load_mode(self):
        if not self.mode == SET_LOAD_MODE:
            self.clear_timers()
            self.igus_slide.retract_load()
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

    def set_scam_angle(self, d_angle):
        ''' 
            Sets the platform to the desire length
        '''
        #d_angle is physical angle we want
        #lenth is the desired extension of the linear actuator
        #pot_value is the desired potentiometer value
        #Doesn't work past 90 but we can't reach that anyways
        length = (d_angle - 63.14478794) / -16.6139526
        pot_value = length * PROPORTION_VALUE
        
        #sets the pot angle to be used in update to actually set the motor
        self.l_actuator_val = pot_value

    def set_scam_speed(self, d_speed):
        #d_speed is the desired speed of the linear actuator.
        #Will be used for maunal control
        
        self.l_actuator_val = d_speed
            
    def scam_in_postion(self, d_angle):
        '''
            Compares current scam position to the expected position
        '''
        #d_angle is physical angle we want
        #lenth is the desired extension of the linear actuator
        #pot_value is the desired potentiometer value
        #Doesn't work past 90 but we can't reach that anyways
        length = (d_angle - 63.14478794) / -16.6139526
        pot_value = length * PROPORTION_VALUE
        
        if self.l_actuator.GetPosition() <= pot_value + OFFSET or \
            self.l_actuator.GetPosition() >= pot_value + OFFSET:
            return True
        else:
            return False
        
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
            if self.l_actuator.GetForwardLimitOK() or self.scam_in_position(LOADING):
                self.mode = LOAD_MODE
        
        if self.mode == LOAD_MODE:
            if self.auto_load and self.igus_slide.has_ball():
                self.shoot_mode()
            
            else:
                self.ball_roller.set(self.ball_roller.OUT)
        #sets the linaer actuator to desired speed or angle depending on the functon called        
        self.l_actuator.Set(self.l_actuator_val)
        
        #update all our components here need updated
        self.ball_roller.update()
        self.igus_slide.update()
        
        
