try:
	import wpilip
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
	'''
		controls the igus slide winch
		motors and sensors:
			winch motor 			for pulling back the ball
			slide limit switch 		make sure the slide is all the way back
			winch solenoid			to use the winch quick release
			slide distance sensor	
			slide optical/distance sensor	
			
	'''
	def __init__(self, igus_motor, igus_limit_switch, igus_solenoid, igus_distance, igus_opt_limit_switch):
		self.igus_motor = igus_motor
		self.igus_limit_switch = igus_limit_switch
		self.igus_solenoid = igus_solenoid
		self.igus_distance = igus_distance
		self.igus_opt_limit_switch = igus_opt_limit_switch
		self.mode = None
		
	def is_ready(self):
		if self.ready == True
			return True
		
	def manual_winch(self, pull_speed):
		self.pull_speed = pull_speed
		self.mode = manual_pull
		
	def release(self):
		self.mode = release
	
	def pull_back(self):
		self.mode = pull_back
	
	def update
		if self.mode == pull_back and self.igus_limit_switch is False:
			self.igus_motor.Set(PULL_BACK_SPEED)
			self.mode = pulling
			
		if self.mode == pulling and self.igus_limit_switch is True:
			self.igus_motor.Set(0)
			self.mode = None
			self.ready = True
			
		if self.mode == release:
			self.igus_solenoid.Set(True)
			self.mode = releasing

		if self.mode == releasing:
			'''make sure ball launches fully before stopping again''' 
			wpilib.wait(BALL_RELEASE_WAIT_TIME)
			self.igus_solenoid.Set(False)
			self.mode = None
			
			
		if self.mode == manual_pull:
			self.igus_motor.Set(self.pull_speed)
			self.mode = None
		