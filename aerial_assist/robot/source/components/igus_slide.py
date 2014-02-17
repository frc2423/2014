try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#import all modes
from common.modes import *


#States    
SHOOT = 0 #next action is to shoot
SHOOTING = 1 #in the process of shooting
SHOT = 2
RETRACT_LOAD = 3
RETRACTED_LOAD = 4
RETRACT_SHOOT = 3
RETRACTED_SHOOT = 4
MANUAL_CONTROL = 5


#ball states
NO_BALL = 0
HAS_BALL = 1
UNKNOWN = 2

#used to determine if ball is actually in the proper sensor location
HAS_BALL = 4

#Constants not definite values yet
RETRACT_SPEED = 1
HAS_SHOT_TIME = 1.5    
SOLENOID_SET_TIME = .5
class IgusSlide(object):
    '''
        controls the igus_slide winch
        motors and sensors:
            igus_motor                 for pulling back the shuttle, it has a forward limit switch
            igus_solenoid            to use the winch quick release; it is a DoubleSolenoid
            igus_distance sensor    for detecting if shuttle is in the correct position
            ball_detector           optical switch for ball detection, used only in loading mode
            shuttle_detector        optical switch to detect the shuttle, only used in loading mode
    '''
    def __init__(self, igus_motor, igus_solenoid, igus_distance, ball_detector, shuttle_detector, auto_mode = AUTO):

        #All limit switches are atttached to jaguars so thaat no longer exists
        self.igus_motor = igus_motor
        self.igus_solenoid = igus_solenoid
        
        #timer used for shooting and waiting for the solenoid to pop in 
        self.timer = wpilib.Timer()

        self.igus_motor_value = 0
        
        self.ball_detector = ball_detector
        
        self.shuttle_detector = shuttle_detector
        
        self.state = None
        
        #used if we are in a blocking state like shooting
        self.next_state = None
        
        #amount of times we have asked for if the ball is actually in the sensor
        #area    
        self.has_ball_count = 0
        
        self.auto_mode = auto_mode
        
    def set_mode(self, mode):
        '''
            sets the mode of the igus_slide
        '''
        if self.auto_mode == AUTO:
            if mode == SHOOT_MODE:
                self._retract_shoot()
                
            elif mode == LOAD_MODE:
                self._retract_load()
                
            elif mode == PASS_MODE:
                #doesn't matter here, but _retract_load is a catch all, if we are
                #past the point of loading we'll just go into shooting position
                #if not well go to our loading position, if the sensor is broken
                #well go to our shooting position.
                self._retract_load()
            
        
    def shoot(self):
        '''
            shoots the ball but only if the limit switch is hit. Unless we have
            overridden the limitswitch if auto_mode = manual - 
            sr todo am I sure about that? maybe some other override varaibles, or
            another functions
        '''
        
        if not self.igus_motor.GetForwardLimitOK() or self.auto_mode == MANUAL:
            self.state = SHOOT
        
    def _retract_load(self):
        '''
            puts us in load mode, unless we are currently in shooting mode
        '''
        
        #can only retract to load if we have just started the match or we just shot
        if self.is_ready_retract():
            self.state = RETRACT_LOAD
        else:
            self.next_state = RETRACT_LOAD

            
    def _retract_shoot(self):
        '''
            puts the robot into shoot mode
        '''
        
        #we can go to shoot mode if we are already shooting
        if self.is_ready_retract():
            self.state = RETRACT_SHOOT
        else:
            self.next_state = RETRACT_SHOOT
        
    def is_ready_shoot(self):
        '''
            lets us know if we are ready to shoot
        '''
        return self.state == RETRACTED_SHOOT
    
    def is_ready_retract(self):
        '''
            tells us if we are ready to retract the shuttle
        '''
        
        #cant retract while still shooting
        if self.state == SHOOTING:
            return False
        elif self.state == SHOT:
            #timer was reset and started when switching to shot mode
            if (self.timer.HasPeriodPassed(SOLENOID_SET_TIME)):
                self.timer.Stop()
                return True
        else:
            return True
        
    def retract(self):
        '''
            This is a manual retract, it will retract with out care about anything
            except if we have recently shot, also setting this puts us into manual
            mode
        '''
        if self.is_ready_retract():
            self.state = MANUAL_CONTROL
            self.igus_motor_value = RETRACT_SPEED
            
            
    def _has_shot(self):
        '''
            determines if we have shot already
        '''
        #sr todo for now just use a dumb timer
        '''
            if self.igus_distance.Get() >= BALL_LAUNCHED_DISTANCE:
        '''    
        #this is always true unless we are in shooting mode, in that case
        #lets check how long ago we have shot
        
        #timer was started transitioning to this mode
        if self.state == SHOOTING:
            #we have shot a long enough time ago
            if self.timer.HasPeriodPassed(HAS_SHOT_TIME):
                self.timer.Stop()
                return True
            '''
                #shuttle still too close   
                else:
                    self._has_shot_timer.Stop()
                    self._has_shot_timer.Reset()
                    return False
            '''
        else:
            return True
       
    def ball_sensor_triggered(self):
        '''
            determines if the ball is ready to be lifted from loading mode into
            shooting mode
        '''
        #only has meaning in loading mode
        if self.state == RETRACTED_LOAD:
            #sensor is off meaning that there is something over the sensor
            if not self.ball_detector.Get():
                if self.has_ball_count == HAS_BALL:
                    return True
                else:
                    #increment are ball checker
                    self.has_ball_count += 1
                    return False
            else:
                self.has_ball_count = 0
                return False
        else:
            #always return false
            return False
    
    def update(self):
        '''
            Updates the igus_slide and any other components that are part of it
        '''
        
        if self.state == RETRACT_SHOOT:
            #GetForwardLimitOK gets the state of the limit switch from the CANJaguar.
            #pulls back the slide until it hits the limit
            if self.igus_motor.GetForwardLimitOK():
    
                self.igus_motor_value = RETRACT_SPEED

            #Motor allowed to run forward when True
            else:
                
                #checks if slide is all the way pulled back
                self.igus_motor_value = 0
                self.state = RETRACTED_SHOOT
                
            
        elif self.state == RETRACT_LOAD:
            #pull back on ball until we are either all the way back or are retract position
            #for now react to distance sensor instantly, some timing mechanism would be better
            #but I really don't like making a new timer for each, it seems like this "delay timing"
            #should be on the sensor object itself. This might be good as a signal, but what I am
            #really looking for is an event listener to attach the sensor too
            #
            #that could be done by having a thread poll the sensor, but that seems like a lot of
            #over head....
            
            if not self.igus_motor.GetForwardLimitOK() or self.shuttle_detector.Get() == False:
                #since we can't get to loading position if we missed it then
                #we will just have to deal with it and say we are in
                #loading position either way
                self.state = RETRACTED_LOAD
                self.igus_motor_value = 0
                #reset sensor count
                self.has_ball_count = 0
            else:
                
                self.igus_motor_value = RETRACT_SPEED
                
            
        elif self.state == SHOOT:
            #pulls us out of gear
            self.igus_solenoid.Set(wpilib.DoubleSolenoid.Value.kForward)
            #start the shoot timer
            self._has_shot_timer.Reset()
            self._has_shot_timer.Start()
            self.state = SHOOTING

        elif self.state == SHOOTING:
            
            #make sure ball launches fully shot before engaging the gear
            if self._has_shot():
                #push us back into gear (note until the motor starts retracting 
                #we may not actually be back in gear
                self.igus_solenoid.Set(wpilib.DoubleSolenoid.Value.kReverse)
                self.state = SHOT
                #reset the timer, but it should keep going
                self.timer.Reset()
            
        #we dont want the shuttle to flap around and not be connected to the winch
        #so lets auto retract it here
        elif self.state == SHOT:
            #set us to our next state (states check if they can retract)
            if self.next_state == RETRACT_SHOOT:
                #go to shoot position because we were asked too
                self._retract_shoot()
            else:
                #go to load position by default
                self._retract_load()
                
            
        #if we are in manual mode out motor value was set before this
        #sets the components of the igus    
        self.igus_motor.Set(self.igus_motor_value)
        
        #reset the motor value of the igus motor
        
        self.igus_motor_value = 0
