try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib
    
angle_max = 360
class Angle(object):
     
    def __init__(self, angle_motor):
        '''init the angle motor ( a CANJaguar) and speed variable( speed of jaguar)'''
        self.angle_motor = angle_motor
        self.speed = 0
        
    def set_speed(self,speed):
        ''' sets the speed that will be set on update'''
        self.speed = speed
    
    def update(self):
        ''' sets the speed on the jaguar'''
        self.angle_motor.Set(self.speed)
    
    