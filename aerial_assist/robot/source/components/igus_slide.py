try:
	import wpilip
except ImportError:
	from pyfrc import wpilib

#States	
shoot = 0 #next action is to shoot
pull_back = 1 #next action
shooting = 3 #in the process of shooting
manual_winch = 4 #manual control of the winch
slow_release = 5 #about to release the slide slowy not sure if possible

#Constants not definite values yet
IGUS_SENSOR_DISTANCE = 1
PULL_BACK_SPEED = 1
BALL_RELEASE_WAIT_TIME = 1
RELEASE_SPEED = -.5

class igus_slide(object):
	'''
		controls the igus slide winch
		motors and sensors:
			igus motor 			for pulling back the ball
			igus limit switch 		make sure the slide is all the way back
			igus solenoid			to use the winch quick release
			igus distance sensor	for detecting if ball is in the correct position
			igus optical sensor	for detecting if slide is in the correct position for loading mode
			
	'''
	def __init__(self, igus_motor, igus_limit_switch, igus_solenoid, igus_distance, igus_opt_limit_switch):
		self.igus_motor = igus_motor
		self.igus_limit_switch = igus_limit_switch
		self.igus_solenoid = igus_solenoid
		self.igus_distance = igus_distance
		self.igus_opt_limit_switch = igus_opt_limit_switch
		self.mode = None
		self.ready = None
	def is_ready(self):
		'returns True if the slide is all the way pulled back and ready to be released'
		if self.igus_limit_switch <= SLIDE_READY_DISTANCE:
			return True
		else:
			return False

	def manual_winch(self, pull_speed):
		'manually controls the winch'
		self.pull_speed = pull_speed
		self.mode = manual_winch
		
	def slow_release(self):
		self.mode = slow_release
		
	def shoot(self):
		self.mode = shoot
	
	def pull_back(self):
		self.mode = pull_back
		
	def ready_to_load(self):
		if self.igus_opt_limit_switch.Get() <= RAIL_LOADING_DISTANCE:
			return True
		
		else:
			return False
	
	def update(self):
		if self.mode == pull_back:
			if self.igus_limit_switch == False:
				self.igus_solenoid.Set(False)
				self.igus_motor.Set(PULL_BACK_SPEED)
			
			
			if self.igus_limit_switch == True:
				self.igus_solenoid.Set(False)
				self.mode = None
				self.ready = True 
			
		elif self.mode == shoot:
			
			self.igus_solenoid.Set(True)
			self.mode = releasing

		elif self.mode == shooting:
			'make sure ball launches fully before stopping again' 
			wpilib.wait(BALL_RELEASE_WAIT_TIME)
			self.igus_solenoid.Set(False)
			self.mode = None
			
			
		elif self.mode == slow_release: 
			if self.igus_slide_opt_limit_switch >= RELEASE_DISTANCE:
				'slowly move the slide forward instead of switching the gear, not sure if possible'
				self.igus_motor.Set(RELEASE_SPEED)
			
			if self.igus_slide_opt_limit_switch <= RELEASE_DISTANCE:
				self.igus_motor.Set(0)
				self.mode = None
		
		elif self.mode == manual_winch:
			'manual control of the winch'
			self.igus_motor.Set(self.pull_speed)
			self.mode = None
		