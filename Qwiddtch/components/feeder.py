try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib

# how long the feed function is locked out for in seconds
FEED_DELAY = .5

# we turn the feeder motor 120 degrees for each ball
FEED_ANGLE_INCREASE = 120

#maximum angle of the motor
FEED_ANGLE_MAX = 360

#angle to reset to
FEED_ANGLE_RESET = 120
class Feeder(object):
    
    def __init__(self, feed_servo):
        '''
            Function: init feeder components
            Variables:
                feed_servo - a PWM controlled VEX motor, treated as a servo
                set_feed - internal feed position to set the VEX servo to
                timer - counter that tells us th
        '''
        
        self.feed_servo = feed_servo
        self.feed_angle = 0
        
        self.timer = None;
    def feed(self):
        '''
            Function: 
                sets the Vex motor desired angle another FEED_ANGLE_INCREASE
                this function will only increase the angle if called after 
                FEED_DELAY seconds after the last call to this function 
        '''
        if self.timer is None or self.timer.HasPeriodPassed(FEED_DELAY):
        
            current = self.feed_angle
            
            if current >= FEED_ANGLE_MAX:
                self.feed_angle = FEED_ANGLE_RESET
            else:
                self.feed_angle = current + FEED_ANGLE_INCREASE
                
            if self.timer is None:
                timer = wpilib.Timer()
                timer.Start()
                
            
    def update(self):
        '''
            Function: updates the actual angle of the motor
        '''
        self.feed_servo.SetAngle(self.feed_angle)
        