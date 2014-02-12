try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#States    
SHOOT = 0 #next action is to shoot
SHOOTING = 1 #in the process of shooting
SHOT = 2
RETRACT = 3
RETRACTED = 4
MANUAL_CONTROL = 5

#Constants not definite values yet
BALL_LAUNCHED_DISTANCE = 1
RETRACT_SPEED = -1
HAS_BALL_TIME = 1
HAS_SHOT_TIME = 1    

class IgusSlide(object):
    '''
        controls the igus_slide winch
        motors and sensors:
            igus_motor                 for pulling back the shuttle, it has a forward limit switch
            ls_retracted             make sure the slide is is_retracted
            igus_solenoid            to use the winch quick release; it is a DoubleSolenoid
            igus_distance sensor    for detecting if shuttle is in the correct position
            os_ball                 optical switch for ball detection, used only in loading mode
    '''
    def __init__(self, igus_motor, igus_solenoid, igus_distance, os_ball):

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
        
        self.os_ball = os_ball
        
    def shoot(self):
        '''
            prepairs the robot to shoot, does not allow us to shoot unless we 
            are in is_retracted mode
        '''
        if self.mode == RETRACTED:
            self.mode = SHOOT
          
    def shut_solenoid(self):
        self.shut_solenoid = True
        
    def is_retracted(self):
        if self.mode == RETRACTED:
            return True
        else:
            return False
    
    def retract(self):
        '''
            puts us in retracted mode, unless we are currently in shooting mode
        '''
        if not self.mode == SHOOTING:
            self.mode = RETRACT

    def has_shot(self):
        '''
            determines if we have shot already
        '''
            #slide is past expected shooting distance
        if self.igus_distance.Get() >= BALL_LAUNCHED_DISTANCE:
            #shuttle has been far enough away for long enough time 
            if self.has_shot_timer.HasPeriodPassed(HAS_SHOT_TIME):
                self.has_shot_timer.Stop()
                return True
            #Timer has not yet started, lets start it
            elif self.has_shot_timer.Get() == 0:
                self.has_shot_timer.Reset()
                self.has_shot_timer.Start()
                return False
        #shuttle still too close   
        else:
            self.has_shot_timer.Stop()
            self.has_shot_timer.Reset()
            return False
    
    def has_ball(self):
        '''
            determines if the ball is ready to be lifted from loading mode into
            shooting mode
        '''
        #sensor is off meaning that there is something over the sensor
        if not self.os_ball.Get():
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
        
        if self.mode == RETRACT:
            
            #pulls back the slide until it hits the limit
            if self.ls_retracted.Get() == False:
    
                self.igus_motor_value = RETRACT_SPEED


            #GetForwardLimitOK gets the state of the limit switch from the CANJaguar.
            #Motor allowed to run forward when True
            elif self.igus_motor.GetForwardLimitOK == False:
                
                #checks if slide is all the way pulled back
                self.igus_motor_value = 0
                self.mode = RETRACTED
            
        elif self.mode == SHOOT:
            #pulls us out of gear
            self.igus_solenoid.Set(wpilib.DoubleSolenoid.Value.kForward)
            self.mode = SHOOTING

        elif self.mode == SHOOTING:
            
            #make sure ball launches fully shot before engaging the gear
            if self.has_shot():
                self.igus_solenoid.Set(wpilib.DoubleSolenoid.Value.kReverse)
                self.mode = SHOT
            
            
        #what is this?   
        if self.shut_solenoid == True:
            self.igus_solenoid.Sets(False)
            self.shut_solenoid = False
            
        #sets the components of the igus    
        self.igus_motor.Set(self.igus_motor_value)
