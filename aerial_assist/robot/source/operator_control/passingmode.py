from common.logitech_util import * 
from components.scam import PASSING_ANGLE

class LoadingMode(object):

    # this name should be descriptive and unique. This will be shown to the user
    # on the SmartDashboard
    MODE_NAME = "Passing Mode"
    
    # Since we expect autonomous to shoot out all our frisbees this should be the 
    # default mode 
    DEFAULT = False


    def __init__(self, components, ds):
        '''
            Constructor
            
            params:components    dictionary of components
            params:ds            driver station instance
        '''
        self.ball_roller = components['ball_roller']
        self.igus_slide = components['igus_slide']
        self.scam = components['scam']
        
        self.ds = ds
        
    def on_enable(self):
        
        #
        # nothing special on enable, set should take care of everything
        #
        pass
    def on_disable(self):
        pass
    
    
    def set(self, auto_load, auto_scam, auto_igus):
        #
        #PASS_MODE actions
        #
        #switch between if we can auto load or not
        
        #
        #Pass the ball by user command
        #
        if stick_button_on(R_BUMPER,self.ds):
            self.ball_roller.roll_out()
        

        #
        # Set the position of the scam first do angle control, set to 0
        # if we are already in the goal range
        #
        if auto_scam:
            self.scam.set_angle(PASSING_ANGLE)
            
    