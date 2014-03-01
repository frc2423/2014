''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#scam motor controls the linear actuator

#import all modes
from common.modes import *

#Variables 
LOADING_ANGLE = -31
SHOOTING_ANGLE = 30 
PASSING_ANGLE = LOADING_ANGLE

class Scam(object):
    
    
    def __init__(self, l_actuator):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           
           l_actuator         linear actuator controls the 4 bar linkage - has a potentiometer attached to it
                              this motor is an angle position jaguar
           
           values used to set real positions of the Scam
           
           l_actuator_val     value to set the l_actuator position, maybe speed or position
        '''
        self.l_actuator = l_actuator    
        self.l_actuator_val= 0
        self.has_passed_timer = wpilib.Timer()
        
        self.sd = wpilib.SmartDashboard
                    
    
    def set_angle(self, d_angle):
        ''' 
            Sets the platform to the desire length
        '''
        self.l_actuator_val = d_angle
        self.l_actuator.set_angle(d_angle)

    def set_speed(self, d_speed):
        
        self.l_actuator_val = d_speed
        self.l_actuator.set_manual_motor_value(d_speed)
            
    def in_position(self):
        '''
            Lets us know if the scam is ready
        '''
        return self.l_actuator.is_ready()
    
    def lowered(self):
        return not self.l_actuator.motor.GetForwardLimitOK()
    
    def _update_smartdashboard(self):
        self.sd.PutNumber("Scam Goal", self.l_actuator_val)
        self.sd.PutNumber("Scam Angle", self.l_actuator.get_position())
        self.sd.PutBoolean("In Position", self.in_position())

    def update(self):
        
        self.l_actuator.update()
        self._update_smartdashboard()
        
        #
        # Clear l_actuators goal/val
        #
        self.l_actuator_val = 0
        
        
