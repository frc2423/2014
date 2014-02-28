from common.logitech_util import * 
from components.scam import LOADING_ANGLE

class LoadingMode(object):

    # this name should be descriptive and unique. This will be shown to the user
    # on the SmartDashboard
    MODE_NAME = "Manual Mode"
    
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
    
    
    #we want all manual actions to be accessible from operator control mode so
    #make them here
    def manual_scam(self):
        if stick_button_on(L_TRIGGER,self.ds):
            man_scam_speed = 1
        elif stick_button_on(L_BUMPER,self.ds):
            man_scam_speed = -1
        else:
            man_scam_speed = 0
        
        self.scam.set_speed(man_scam_speed)
        
    def manual_igus(self):
        self.igus_slide.set_manual()
        if stick_button_on(4,self.ds):
            self.igus_slide.retract()
            
        #
        # If igus rail is manual we should make shooting manual.
        #
            
        if stick_button_on(R_TRIGGER,self.ds):
            self.igus_slide.shoot(override = stick_button_on(R_BUMPER , self.ds))
            
        
    def set(self, auto_load, auto_scam, auto_igus):
        '''
            Do all manual actions
        '''
        self.manual_igus()
        self.manual_scam()
        
        
