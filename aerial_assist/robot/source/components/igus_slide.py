try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

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


#Constants not definite values yet
BALL_LAUNCHED_DISTANCE = 1
RETRACT_SPEED = 1
HAS_BALL_TIME = 1
HAS_SHOT_TIME = 1    

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
    def __init__(self, igus_motor, igus_solenoid, igus_distance, ball_detector, shuttle_detector):

        #All limit switches are atttached to jaguars so thaat no longer exists
        self.igus_motor = igus_motor
        self.igus_solenoid = igus_solenoid
        #what is this?
        self.shut_solenoid = False
        
        #timer for how long we have had the ball under the 
        self.has_ball_timer = wpilib.Timer()
        #timer for how time
        self.has_shot_timer = wpilib.Timer()
        self.igus_motor_value = 0
        
        self.ball_detector = ball_detector
        
        self.shuttle_detector = shuttle_detector
        
        self.mode = None
        
    def shoot(self):
        '''
            prepairs the robot to shoot, does not allow us to shoot unless we 
            are in is_retracted mode
        '''
        if self.mode == RETRACTED_SHOOT:
            self.mode = SHOOT
          
        
    def retract_load(self):
        '''
            puts us in load mode, unless we are currently in shooting mode
        '''
        
        #can only retract to load if we have just started the match or we just shot
        if self.mode != SHOOTING:
            self.mode = RETRACT_LOAD
            
    def retract_shoot(self):
        '''
            puts the robot into shoot mode
        '''
        
        #we can go to shoot mode from any mode but shooting
        if self.mode != SHOOTING:
            self.mode = SHOOT
        
    def retract(self):
        '''
            This is a manual retract, it will retract with out care about anything
            except if we have recently shot, also setting this puts us into manual
            mode
        '''
        if self.has_shot():
            self.mode = MANUAL_CONTROL
            self.igus_motor_value = RETRACT_SPEED
            
    def has_shot(self):
        '''
            determines if we have shot already
        '''
        #sr todo for now just use a dumb timer
        '''
            if self.igus_distance.Get() >= BALL_LAUNCHED_DISTANCE:
        '''    
        #this is always true unless we are in shooting mode, in that case
        #lets check how long ago we have shot
        
        if self.mode == SHOOTING:
            #shuttle has been far enough away for long enough time 
            if self.has_shot_timer.HasPeriodPassed(HAS_SHOT_TIME):
                self.has_shot_timer.Stop()
                return True
            '''
                #shuttle still too close   
                else:
                    self.has_shot_timer.Stop()
                    self.has_shot_timer.Reset()
                    return False
            '''
        else:
            return True
       
    def ball_sensor_triggered(self):
        '''
            determines if the ball is ready to be lifted from loading mode into
            shooting mode
        '''
    
        #sensor is off meaning that there is something over the sensor
        if not self.ball_detector.Get():
            #something has been over the sensor for at lease HAS_BALL_TIME,
            # lets assume that its actually a ball
            if self.has_ball_timer.HasPeriodPassed(HAS_BALL_TIME):
                self.has_ball_timer.Stop()
                return True
            #Timer has not yet started, lets start it
            elif self.has_ball_timer.Get() == 0:
                self.has_ball_timer.Reset()
                self.has_ball_timer.Start()
                return False
        #the sensor is on because nothing is on it. reset the timer       
        else:
            self.has_ball_timer.Stop()
            self.has_ball_timer.Reset()
            return False
    
    def update(self):
        '''
            Updates the igus_slide and any other components that are part of it
        '''
        
        if self.mode == RETRACT_SHOOT:
            #GetForwardLimitOK gets the state of the limit switch from the CANJaguar.
            #pulls back the slide until it hits the limit
            if self.igus_motor.GetForwardLimitOK():
    
                self.igus_motor_value = RETRACT_SPEED

            #Motor allowed to run forward when True
            else:
                
                #checks if slide is all the way pulled back
                self.igus_motor_value = 0
                self.mode = RETRACTED_SHOOT
                
            
        elif self.mode == RETRACT_LOAD:
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
                self.mode = RETRACTED_LOAD
                self.igus_motor_value = 0
            
            else:
                
                self.igus_motor_value = RETRACT_SPEED
                
            
        elif self.mode == SHOOT:
            #pulls us out of gear
            self.igus_solenoid.Set(wpilib.DoubleSolenoid.Value.kForward)
            #start the shoot timer
            self.has_shot_timer.Reset()
            self.has_shot_timer.Start()
            self.mode = SHOOTING

        elif self.mode == SHOOTING:
            
            #make sure ball launches fully shot before engaging the gear
            if self.has_shot():
                #push us back into gear (note until the motor starts retracting 
                #we may not actually be back in gear
                self.igus_solenoid.Set(wpilib.DoubleSolenoid.Value.kReverse)
                self.mode = SHOT
                #stop and reset the timers
                self.has_shot_timer.Stop()
                self.has_shot_timer.Reset()
            
            
        #if we are in manual mode out motor value was set before this
        #sets the components of the igus    
        self.igus_motor.Set(self.igus_motor_value)
        
        #reset the motor value of the igus motor
        
        self.igus_motor_value = 0
