''' the scam represents the four-bar-linkage on the robot, it will control the linear actuator'''

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
    
class scam(object):
    
    def __init__(self, scam_motor, scam_pot):
        self.scam_motor = scam_motor    
        self.scam_pot = scam_pot
    
    def move(self, move_speed):
        self.move_speed = move_speed
    
    def set_angle(self, angle, speed):
        self.angle = angle
        self.speed = speed
        
    def update(self):
        
        if self.angle is not None:
            if self.scam_pot.Get() > self.angle:
                self.scam_motor.Set(self.speed)
            elif self.scam_pot.Get() < self.angle:
                self.scam_motor.Set(self.speed * -1)
        elif self.move_speed is not None:
            self.scam_motor.Set(self.move_speed)
            