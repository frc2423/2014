try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib
    
class shooter(object):
    '''Controls the shooter wheel'''
    
    def __init__(self, shooter_jag):
        
        self.shooter_jag = shooter_jag
        
    def set_speed(self, d_speed):
        self.d_speed = d_speed
        self.set_speed = d_speed
        
    def update(self):
        self.shooter_jag.set_speed(self.set_speed)
        
    



    
