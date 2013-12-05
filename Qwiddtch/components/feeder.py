try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib
    
class feeder(object):
    
    def __init__(self, feed_servo):
        self.feed_servo = feed_servo
        self.set_feed = 0
    
    def feed(self):
        current = self.feed_servo.get_angle()
        if current >= 300:
            self.set_feed = 120
        else:
            self.set_feed = current + 120
            
    def update(self):
        self.feed_servo.set_angle(self.set_feed)
        