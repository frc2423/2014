''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#scam motor controls the linear actuator

#import robot modes
from common.modes import *

#Variables 
'''place holders for now'''
ANGLE_SPEED = 1
LOADING_ANGLE = 0
SHOOTING_ANGLE = 1
PASSING_ANGLE = 0
HAS_PASSED_TIME = 1

class RobotSystem(object):
    
    def __init__(self, scam, igus_slide, ball_roller):
        
        '''
           Controls the 4 bar linkage with the linear actuator
           
           scam               instances of the scam, controls angle control
           igus_slide         instance of the igus_slide, controls the winch
           ball_roller        instance of the ball_roller, moves the balls on and off the slide
           
           values used to set real positions of the Scam
           
           l_actuator_val     value to set the l_actuator position, maybe speed or position
        '''
        self.scam = scam    
        self.igus_slide = igus_slide
        self.ball_roller = ball_roller
        
        self.components = [ self.scam, self.igus_slide, self.ball_roller ]
        
        self.mode = None
        
    def get_mode(self):
        return self.mode    
    
    def set_mode(self, mode):
        '''
            sets everything to desired mode, components not in auto mode shall 
            do nothing on this command
        '''
        if not self.mode == mode:
            self.mode = mode
            for component in self.components:
                component.set_mode(mode)
     
     
    #
    # Manual Controls
    #        
    def shoot(self):
        '''
            Shoots the igus_slide, igus slide figures out if its ready
        '''
        self.igus_slide.shoot()
        
    def ball_roll(self, direction):
        '''
            moves the ball roller in the desired direction
        '''
        self.ball_roller.set(direction)
        
    def retract_slide(self):
        self.igus_slide.retract()
        
    def move_scam(self, move_val):
        self.scam.set_scam_speed(move_val)


    def do_auto_actions(self):
        '''
            This function uses the values of the different components and our current
            state to determine what to do next if we are in auto_mode the only action 
            we have right now is auto load
        '''
        
        #must be in loading mode and every component in auto mode 
        if self.mode == LOADING_MODE and sum([component.auto_mode == AUTO for \
                                                 component in self.components]):
            
            if self.igus_slide.ball_sensor_triggered():
                #ball has been detected set ourselves to shooting mode
                self.set_mode(SHOOT_MODE)
