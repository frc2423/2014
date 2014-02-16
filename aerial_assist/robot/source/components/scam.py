''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#scam motor controls the linear actuator

#import all modes
from common.modes import *

#Variables 
LOADING_ANGLE = -15
SHOOTING_ANGLE = 45
PASSING_ANGLE = LOADING_ANGLE

class Scam(object):
    
    
    def __init__(self, l_actuator, auto_mode = AUTO):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           
           l_actuator         linear actuator controls the 4 bar linkage - has a potentiometer attached to it
                              this motor is an angle position jaguar
           
           values used to set real positions of the Scam
           
           l_actuator_val     value to set the l_actuator position, maybe speed or position
        '''
        self.l_actuator = l_actuator    
        self.l_actuator_val = None
        self.has_passed_timer = wpilib.Timer()
        self.auto_mode = auto_mode
        
    def set_mode(self, mode):
        '''
            sets the mode of the scam
        '''
        if self.auto_mode == AUTO:
            if mode == SHOOT_MODE:
                self.set_scam_angle(SHOOTING_ANGLE)
                
            elif mode == LOAD_MODE:
                self.set_scam_angle(LOADING_ANGLE)
                
            elif mode == PASS_MODE:
                self.set_scam_angle(PASSING_ANGLE)
            
    
    def set_scam_angle(self, d_angle):
        ''' 
            Sets the platform to the desire length
        '''
        self.l_actuator_val = d_angle
        self.l_actuator.set_angle(d_angle)

    def set_scam_speed(self, d_speed):
        #d_speed is the desired speed of the linear actuator.
        #Will be used for maunal control
        
        self.l_actuator_val = d_speed
        self.l_actuator.set_manual_motor_value(d_speed)
            
    def scam_in_postion(self, d_angle):
        '''
            Compares current scam position to the expected position
        '''
        return self.l_actuator.is_ready()
    
    def update(self):
        
        self.l_actuator.update()
        
        
