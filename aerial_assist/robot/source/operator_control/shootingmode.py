from common.logitech_util import * 
from components.scam import SHOOTING_ANGLE

class LoadingMode(object):

    # this name should be descriptive and unique. This will be shown to the user
    # on the SmartDashboard
    MODE_NAME = "Shooting Mode"
    
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
            set platform to shooting mode
        '''
        #
        #while we are not in position the ball rollers should keep feeding
        #the ball in
        #
        
        self.ball_roller.roll_in()
        #
        # Set the position of the scam first do angle control, set to 0
        # if we are already in the goal range
        #
        
        if auto_scam: 
            self.scam.set_angle(SHOOTING_ANGLE)
            # we are in position, stop using PID, were better without it
            if self.scam.in_position():
                self.scam.set_speed(0)
                #we are in position ball rollers don't need to be rolled in
                #any more
                self.ball_roller.off()
            
        #
        #Retract to shooting position, if we are not already there
        #
        if auto_igus:    
            self.igus_slide.retract_shoot()
            
        #
        #shoot if trigger is hit, user can shoot at any point by pressing both triggers
        #igus_slide will automatically try to shoot
        #
        
        if stick_button_on(R_TRIGGER,self.ds):
            self.igus_slide.shoot(override = stick_button_on(R_BUMPER,self.ds))
