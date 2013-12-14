try:
	import wpilib 
except ImportError:
	import fake_wpilib as wpilib

#
#Import all systems and components here
#
from components.angle import angle
from components.feeder import feeder
from components.shooter import shooter
  

#
#Declare all the ports and channels here
#Note: these are shared between the electrical test and main code!
#

#CAN channels
shooter_wheel_can = 1

#Jaguar channels
angle_wheel_jag = 1
feeder_wheel_jag = 2

#Joystick Channels
joystick_channel_one = 1

#Joysticks
joystick_one = wpilib.Joystick(joystick_channel_one)
#
#Create motors/sensors here
#

shooter_wheel = wpilib.CANJaguar(shooter_wheel_can)
angle_wheel = wpilib.Jaguar(angle_wheel_jag)
feeder_wheel = wpilib.Jaguar(feeder_wheel_jag)


#Variables
set_angle = 0
pressed = 1

#Joystick buttons and axis
joystick_one_x = joystick_one.GetX()
joystick_one_y = joystick_one.GetY()
joystick_one_throttle = joystick_one.GetThrottle()
joystick_one_trigger = joystick_one.GetTrigger()


class MyRobot (wpilib.SimpleRobot):
	def __init__(self):
		wpilib.SimpleRobot.__init__(self)
		
		self.ds = wpilib.DriverStation.GetInstance()
		#might have SmartDashboard maybe not. All Smart Dashboard things will be commented out
		#self.sd = wpilib.SmartDashboard
		
		
		
		#create component instances
		'''ex self.my_feeder = Feeder(feeder_motor, 
		frisbee_sensor, 
		feeder_sensor)'''
		self.my_feeder = feeder(feeder_wheel)
		self.my_angle = angle(angle_wheel)
		self.my_shooter = shooter(shooter_wheel)
		
		#create system instances
			#ex self.my_auto_targeting = AutoTargeting(self.my_robot_turner, self.my_shooter_platform, self.my_target_detector)
		
		
		
		
		#In the 2013 code we had a dictionary of autonomous mode components. I'm assuming we are keeping that.
		
		
		#initialize other needed SmartDashboard imputs if we use it. This would be real competition stuff.
		
		
	def RobotInit(self):
		pass
	
	def Disabled(self):
		print("MyRobot::Autonomous()")
		
		#self.sd.PutNumber("Robot Mode", self.MODE_DISABLED)
		
		
	def Autonomous(self):		
		print("MyRobot::Autonomous()")

		#self.sd.PutNumber("Robot Mode", self.MODE_AUTONOMOUS)

		
	def OperatorControl(self):
		print("MyRobot::OperatorControl()")

		#self.sd.PutNumber("Robot Mode", self.MODE_TELEOPERATED)
		
			#
		#angle
		#
		'''no definitive plan for angle control'''
		
		#
		#shooter
		#
		self.d_speed = joystick_one_throttle
		shooter.set_speed(self, self.d_speed)

		#
		#feeder
		#
		if joystick_one_trigger == pressed:
			feeder.feed()
			
		# set the watch dog
		dog = self.GetWatchdog()
		dog.SetEnabled(False)
		dog.SetExpiration(0.25)
		
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


