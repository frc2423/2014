try:
	import wpilib
'''Controls the slide that ball is on, includes winch that pulls back ball'''

except ImportError:
	from pyfrc import wpilib

#States	
release = 0
pull_back = 1
pulling = 2
releasing = 3
manual_pull = 4

#Constants
'''these are not final yet, just place holders'''
IGUS_SENSOR_DISTANCE = 1
PULL_BACK_SPEED = 1
BALL_RELEASE_WAIT_TIME = 1

class igus_slide(object):
	
	def __init__(self, igus_motor, igus_limit_switch, igus_solenoid, igus_distance, igus_opt_limit_switch):
		self.igus_motor = igus_motor
		self.igus_limit_switch = igus_limit_switch
		self.igus_solenoid = igus_solenoid
		self.igus_distance = igus_distance
		self.igus_opt_limit_switch = igus_opt_limit_switch
		self.mode = None
		
	def manual_winch(self, pull_speed):
		self.pull_speed = pull_speed
		self.mode = manual_pull
		
	def release
		self.mode = release
	
	def pull_back(self):
		self.mode = pull_back
	
	def update
		if self.mode == pull_back and self.igus_distance >= IGUS_SENSOR_DISTANCE:
			self.igus_motor.Set(PULL_BACK_SPEED)
			self.mode = pulling
			
		if self.mode == pulling and self.igus_distance <= IGUS_SENSOR_DISTANCE:
			self.igus_motor.Set(0)
			
		if self.mode == release:
			self.igus_solenoid.Set(True)
			self.mode = releasing
		
		if self.mode == releasing
			'''make sure ball launches fully before stopping again''' 
			wpilib.wait(BALL_RELEASE_WAIT_TIME)
			self.mode = None
			
		if self.mode == manual_pull:
			self.igus_motor.Set(self.pull_speed)
			self.mode = None
		