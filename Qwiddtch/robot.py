try:
    import wpilib 
except ImportError:
    import fake_wpilib as wpilib

#
#Import all systems and components here
#



#
#Declare all the ports and channels here
#Note: these are shared between the electrical test and main code!
#

#CAN channels
shooter_wheel_can = 1

#Jaguar channels
angle_wheel_jag = 1
feeder_wheel_jag = 2

#
#Create motors/sensors here
#

shooter_wheel = wpilib.CANJaguar(shooter_wheel_can)
angle_wheel = wpilib.Jaguar(angle_wheel_jag)
feeder_wheel = wpilib.Jaguar(feeder_wheel_jag)


#Variables
set_spd = 0
set_angle = 0



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
        
        
        # set the watch dog
        dog = self.GetWatchdog()
        dog.SetEnabled(False)
        dog.SetExpiration(0.25)


