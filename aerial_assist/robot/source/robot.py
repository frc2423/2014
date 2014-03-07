try:
	import wpilib
except ImportError:
	from pyfrc import wpilib

#common imports
from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3, GP2D120
from common.ez_can_jaguar import EzCANJaguar 
from common.auto_jaguar import AnglePositionJaguar
from common.ws2801 import ws2801_led
from common.modes import *
import common.logitech_controller as lt

#component imports
from components.ball_roller import BallRoller
import components.ball_roller as bl
from components.igus_slide import IgusSlide,RELEASE, ENGAGE
from components.scam import Scam, LOADING_ANGLE, SHOOTING_ANGLE, PASSING_ANGLE

#Operator control Manager
from operator_control import OperatorControlManager

#Constants
CONTROL_LOOP_WAIT_TIME = .025
TRIGGER_THRESHOLD = .25

#Jag channels (PWM)
front_left_channel = 2
front_right_channel = 1
back_left_channel = 4
back_right_channel = 3
ball_roller_motor = 5

#Digital IO
led_spi_bus = 4
led_spi_clk = 5
compressor_switch = 6

#sensor channels analog
shuttle_mb10x3_port = 1
left_mb10x3_port = 2
right_mb10x3_port = 3
ball_optical = 4
shuttle_optical = 5

#CAN channels 
igus_can = 1
l_actuator_can = 2

#solenoid channels
solenoid1 = 1
solenoid2 = 2

#relay channels
compressorRelayChannel = 6
camera_led_relay_port = 7
ball_roller_relay_port = 5

#LED
led_strip_length = 36

#Joystick channel
joystick_channel = 1

#PID configs taken from 2013 code, similar mechanism for control, needs to be tested
SCAM_P = 3000
SCAM_I = .1
SCAM_D = 14

#guess based on specs todo fix this based on emperical data
THRESHOLD = .045 #position in degrees
ANGLE_MAX_POSITION = .757
ANGLE_MIN_POSITION = .042
ANGLE_MIN_ANGLE = 65
ANGLE_MAX_ANGLE = -30

#Time for autonomous 
AUTO_TIME = 10
AUTO_DRIVE_TIME = 1.6
AUTO_DRIVE_START = 1
AUTO_SHOOT_DELAY = 3
class MyRobot(wpilib.SimpleRobot):
	
	# keep in sync with driver station
	MODE_DISABLED	   = 1
	MODE_AUTONOMOUS	 = 2
	MODE_TELEOPERATED   = 3
	
	def __init__(self):
		
		wpilib.SimpleRobot.__init__(self)
		
		#initilize all basic types( sensors, motors, stuuf like that)
		
		#LED SPI DigitalOutputs
		self.spi_clock = wpilib.DigitalOutput(led_spi_clk)
		self.spi_bus = wpilib.DigitalOutput(led_spi_bus)
		
		#LED SPI
		#self.led_spi = wpilib.SPI(self.spi_clock, self.spi_bus)
		
		#LED
		#self.led_strip  = ws2801_led(led_strip_length, self.led_spi)
		
		#Drive jags
		self.front_left_jag =  wpilib.Jaguar(front_left_channel)
		self.front_right_jag = wpilib.Jaguar(front_right_channel)
		self.back_left_jag =   wpilib.Jaguar(back_left_channel)
		self.back_right_jag =  wpilib.Jaguar(back_right_channel)

		#DoubleSolenoid config 
		self.motor_release_solenoid = wpilib.DoubleSolenoid(solenoid1, solenoid2)
		
		#Compressor
		self.compressor = wpilib.Compressor(compressor_switch, compressorRelayChannel)
		
		# relay
		self.camera_led = wpilib.Relay(camera_led_relay_port)
		self.camera_led.Set(wpilib.Relay.kForward)
		
		ball_roller_relay = wpilib.Relay(ball_roller_relay_port)
		
		#Joystick
		self.logitech = wpilib.Joystick(joystick_channel)

		#CAN jags
		#igus is operated on percent vbus no extra setup is needed
		self.igus_motor = EzCANJaguar(igus_can)
		
		#l_actuator setup
		self.l_actuator = EzCANJaguar(l_actuator_can)
		self.l_actuator.SetPositionReference(wpilib.CANJaguar.kPosRef_Potentiometer)
		#guess on number of turns, but it should be treated as one turn anyway
		self.l_actuator.ConfigPotentiometerTurns(1)
		self.l_actuator.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Brake)
		self.l_actuator.SetPID(SCAM_P, SCAM_I, SCAM_D)
		
		self.l_actuator_auto = AnglePositionJaguar(self.l_actuator, THRESHOLD, ANGLE_MIN_POSITION, ANGLE_MAX_POSITION, ANGLE_MIN_ANGLE, ANGLE_MAX_ANGLE)
		
		
		#sensors
		self.shuttle_distance_sensor = GenericDistanceSensor(shuttle_mb10x3_port, MB10X3)
		self.left_distance_sensor = GenericDistanceSensor(left_mb10x3_port, MB10X3)
		self.right_distance_sensor = GenericDistanceSensor(right_mb10x3_port, MB10X3)
		
		self.ball_detector = GenericDistanceSensor(ball_optical, GP2D120)
		#geuss at average sampling 
		self.ball_detector.SetAverageBits(8)
		self.shuttle_detector = GenericDistanceSensor(shuttle_optical, GP2D120)
		
		self.ds = wpilib.DriverStation.GetInstance()
		self.sd = wpilib.SmartDashboard
		
		self.robot_drive = wpilib.RobotDrive(self.front_left_jag, self.back_left_jag, self.front_right_jag, self.back_right_jag)
		
		
		
		#create components
		self.ball_roller = BallRoller(ball_roller_relay)
		self.igus_slide  = IgusSlide(self.igus_motor, self.motor_release_solenoid, self.shuttle_distance_sensor, self.ball_detector, self.shuttle_detector)  
		self.scam = Scam(self.l_actuator_auto)
		
		# autonomous mode needs a dict of components
		components = {
			# components 
			'ball_roller': self.ball_roller,
			'igus_slide': self.igus_slide,
			'scam': self.scam, 
		}
		
		self.components = []
		self.components = [v for v in components.values() if hasattr(v, 'update')]
		self.operator_control_mode = OperatorControlManager(components, self.robot_drive, self.ds)
		
		#
		#determines if we are to automatically switch states from loading to shooting
		#
		self.mode = None
		
		#init smart dashboard variables
		self.sd.PutBoolean('auto igus', True)
		self.sd.PutBoolean('auto scam', True)
		self.sd.PutBoolean('auto load', False)
		
		
	def RobotInit(self):
		pass
		
	def Disabled(self):
		print("MyRobot::Disabled()")
		
		self.sd.PutNumber("Robot Mode", self.MODE_DISABLED)
	
		while self.IsDisabled():
			wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
			
	def Autonomous(self):		
		print("MyRobot::Autonomous()")
		auto_timer = wpilib.Timer()
		delay = PreciseDelay(CONTROL_LOOP_WAIT_TIME)
		self.sd.PutNumber("Robot Mode", self.MODE_AUTONOMOUS)
		has_shot = False
		self.compressor.Start()
		while self.IsAutonomous() and self.IsEnabled():
			if auto_timer.Get() == 0:
				auto_timer.Start()
				self.igus_slide.retract_shoot()
				self.scam.set_angle(SHOOTING_ANGLE)
				
			elif auto_timer.Get() < AUTO_DRIVE_TIME:
				self.robot_drive.MecanumDrive_Cartesian(0, -.5, 0)	
				
			elif auto_timer.Get() < 4:
				#need to wait till the igus retracts
				pass
				
			elif auto_timer.Get() <5:
				#set motor to stop angle
				self.scam.set_speed(0)
				
			elif has_shot == False:
				self.robot_drive.MecanumDrive_Cartesian(0, 0, 0,)
				self.igus_slide.shoot(True)
				has_shot = True
					
			
			self.update()		
			delay.wait()

	def OperatorControl(self):
		print("MyRobot::OperatorControl()")

		self.sd.PutNumber("Robot Mode", self.MODE_TELEOPERATED)
		self.delay = PreciseDelay(CONTROL_LOOP_WAIT_TIME)

		# set the watch dog
		dog = self.GetWatchdog()
		dog.SetExpiration(0.25)
		dog.SetEnabled(True)
		
		#star compressor
		self.compressor.Start()
		# All operator control functions are now in OperatorControlManager   
		self.operator_control_mode.run(self, CONTROL_LOOP_WAIT_TIME)
		
		dog.SetEnabled(False)
	def update(self):
		for component in self.components:
			component.update()
			
def run():
	
	# this is initialized in StartCompetition, but one of our
	# constructors might use it, and crash
	wpilib.SmartDashboard.init()
	
	robot = MyRobot()
	robot.StartCompetition()
	
	return robot

# this is used for testing
if __name__ == '__main__':
	wpilib.run()
	