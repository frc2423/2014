try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib
    
angle_max = 360
class angle(object):
     
    def __init__(self, angle_servo):
        self.angle_servo = angle_servo
    
    def angle_set(d_angle):
        self.d_angle = d_angle
        self.set_angle = angle_max - d_angle
    
    def update():
        self.angle_servo.set_angle(self.d_angle)
    
    