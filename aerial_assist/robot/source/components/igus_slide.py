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

#Constants not definite values yet
BALL_LAUNCHED_DISTANCE = 1
RETRACT_SPEED = -1
HAS_BALL_TIME = 1
HAS_SHOT_TIME = 1    

class igus_slide(object):
    '''
        controls the igus_slide winch
        motors and sensors:
            igus_motor                 for pulling back the ball
            os_rear                    used to know when the slide is all the way bacl
            ls_retracted             make sure the slide is is_retracted, used when os_rear fails
            igus_solenoid            to use the winch quick release it is a DoubleSolenoid
            igus_distance sensor    for detecting if ball is in the correct position
    '''
    def __init__(self, igus_motor, igus_limit_switch, igus_solenoid, igus_distance, os_rear):


        self.igus_motor = igus_motor
        self.igus_limit_switch = igus_limit_switch
        self.igus_solenoid = igus_solenoid
        self.igus_distance = igus_distance
        self.os_rear = os_rear
        self.shut_solenoid = False
        self.has_ball_timer = wpilib.Timer()
        self.has_shot_timer = wpilib.Timer()
        self.igus_motor_value = 0
        
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
        if not self.os_front.Get():
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
            
            #pulls back the slide until it hits the limit switch
            if self.ls_retracted.Get() == False or self.os_rear.Get():
    
                self.igus_motor_value = RETRACT_SPEED
            
            elif self.igus_limit_switch == True or not self.os_rear.Get():
                
                #checks if slide is all the way pulled back
                self.igus_motor_value = 0
                self.mode = RETRACTED
            
        elif self.mode == SHOOT:
            #pulls us out of gear
            self.igus_solenoid.Set(DoubleSolenoid.Value.kForward)
            self.mode = SHOOTING

        elif self.mode == SHOOTING:
            
            #make sure ball launches fully shot 0before engaging the gear
            if self.has_shot():
                self.igus_solenoid.Set(DoubleSolenoid.Value.kReverse)
                self.mode = SHOT
            
            
        #what is this?   
        if self.shut_solenoid == True:
            self.igus_solenoid.Sets(False)
            self.shut_solenoid = False
            
        #sets the components of the igus    
        self.igus_motor.Set(self.igus_motor_value)