try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib
    
class angle(object):
     
    def __init__(self, angle_servo):
        self.angle_servo = angle_servo
    
    def angle_set(d_angle):
        self.d_angle = d_angle
    
    def update():
        self.angle_servo.set_angle(self.d_angle)
    
    