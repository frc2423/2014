try:
	import wpilip
except ImportError:
	from pyfrc import wpilib

#States	
SHOOT = 0 #next action is to shoot
PULL_BACK = 1 #next action
SHOOTING = 3 #in the process of shooting

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
			igus optical limit	for detecting if slide is in the correct position for loading mode
			
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
		if self.igus_limit_switch == True:
			return True
		else:
			return False
		
	def shoot(self):
		self.mode = SHOOT
	
	def pull_back(self):
		self.mode = PULL_BACK
		
	def ready_to_load(self):
#Maybe should have if not ready to load put the slide down until it hits the limit switch. Also check scam.
		return self.igus_opt_limit_switch.Get()
	
	def update(self):
#Seems that we want it to stop when it hits the optical limit switch and then the mechanical limit switch is back up from what I understand
		if self.mode == PULL_BACK:
			'pulls back the slide until it hits the limit switch'
			if self.igus_limit_switch == False:
				self.igus_motor.Set(PULL_BACK_SPEED)
			
			
			elif self.igus_limit_switch == True:
				'checks if slide is all the way pulled back, and makes sure solenoid is off/closed'
				self.igus_motor.Set(0)
				self.igus_solenoid.Set(False)
				self.mode = None
			
		elif self.mode == SHOOT:
			self.igus_solenoid.Set(True)
			self.mode = SHOOTING

		elif self.mode == SHOOTING:
#What are you even trying to do here? Should be a timer object if you want a delay not a wpilib.wait function
			'make sure ball launches fully before stopping again' 
			wpilib.wait(BALL_RELEASE_WAIT_TIME)
			self.igus_solenoid.Set(False)
			self.mode = None