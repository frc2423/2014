try:
	import wpilib
except ImportError:
	from pyfrc import wpilib

#States	
SHOOT = 0 #next action is to shoot
SHOOTING = 1 #in the process of shooting
SHOT = 2
RETRACT = 3
RETRACTED = 4

#Constants not definite values yet
BALL_LAUNCHED_DISTANCE = 1
PULL_BACK_SPEED = -1
HAS_BALL_TIME = 1	

class igus_slide(object):
	'''
		controls the igus_slide winch
		motors and sensors:
			igus_motor 				for pulling back the ball
			os_rear					used to know when the slide is all the way bacl
			ls_retracted 			make sure the slide is retracted, used when os_rear fails
			igus_solenoid			to use the winch quick release
			igus_distance sensor	for detecting if ball is in the correct position
	'''
	def __init__(self, igus_motor, igus_limit_switch, igus_solenoid, igus_distance, os_rear):
		self.igus_motor = igus_motor
		self.igus_limit_switch = igus_limit_switch
		self.igus_solenoid = igus_solenoid
		self.igus_distance = igus_distance
		self.os_rear = os_rear
		self.shut_solenoid = False
		self.has_ball_timer = wpilib.Timer()
		
	def shoot(self):
		self.mode = SHOOT
	
	def shut_solenoid(self):
		self.shut_solenoid = True
		
	def retracted(self):
		if self.mode == RETRACTED:
			return True
		else:
			return False
		
	
	def retract(self):
		self.mode = RETRACT
	
	def has_ball(self):
		
		if not self.os_front.Get():
			if self.has_ball_timer.HasPeriodPassed(HAS_BALL_TIME):
				self.has_ball_timer.Stop()
				return True
			
			elif self.has_ball_timer.Get() == 0:
				self.has_ball_timer.Reset()
				self.has_ball_timer.Start()
				
		else:
			self.has_ball_timer.Stop()
			self.has_ball_timer.Reset()
			
	def update(self):
		if self.mode == RETRACT:
			
			'pulls back the slide until it hits the limit switch'
			if self.igus_limit_switch == False or self.os_rear.Get():
	
				self.igus_motor.Set(PULL_BACK_SPEED)
			
			elif self.igus_limit_switch == True or not self.os_rear.Get():
				
				'checks if slide is all the way pulled back, and makes sure solenoid is off/closed'
				self.igus_motor.Set(0)
				self.mode = RETRACTED
			
		elif self.mode == SHOOT:
			
			self.igus_solenoid.Set(True)
			self.mode = SHOOTING

		elif self.mode == SHOOTING:
			
			'make sure ball launches fully before stopping again' 
			if self.igus_distance.Get() >= BALL_LAUNCHED_DISTANCE:
				self.igus_solenoid.Set(False)
				self.mode = SHOT
			
		if self.shut_solenoid == True:
			self.igus_solenoid.Sets(False)
			self.shut_solenoid = False