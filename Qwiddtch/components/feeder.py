try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib

feed_angle_increase = 120
feed_angle_max = 360
feed_angle_reset = 120
class feeder(object):
    
    def __init__(self, feed_servo):
        self.feed_servo = feed_servo
        self.set_feed = 0
    
    def feed(self):
        current = self.feed_servo.get_angle()
        if current >= self.feed_angle_max:
            self.set_feed = self.feed_angle_reset
        else:
            self.set_feed = current + feed_angle_increase
            
    def update(self):
        self.feed_servo.set_angle(self.set_feed)
        