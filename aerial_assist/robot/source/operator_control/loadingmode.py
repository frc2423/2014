from common.logitech_util import * 
from components.scam import LOADING_ANGLE

class LoadingMode(object):

    # this name should be descriptive and unique. This will be shown to the user
    # on the SmartDashboard
    MODE_NAME = "Loading Mode"
    
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
        '''
            set platform to zero and climber to lowered
        '''
        #
        #Auto feed the ball
        #
        if self.scam.lowered():
            self.ball_roller.roll_in()
        
        #
        # Set the position of the scam first do angle control, the limit switch
        # shall tell us to stop
        #
        if auto_scam:
            self.scam.set_angle(LOADING_ANGLE)
            
        if auto_igus:    
            self.igus_slide.retract_load()
        
        #if auto load is active return our next mode
        if auto_load:
            if (self.igus_slide.ball_sensor_triggered()):
                return "Shooting Mode"
