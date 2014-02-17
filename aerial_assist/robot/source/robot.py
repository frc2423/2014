try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#common imports
from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3
from common.ez_can_jaguar import EzCANJaguar 
from common.auto_jaguar import AnglePositionJaguar
from common.modes import *
import common.logitech_controller as lt

#component imports
from components.ball_roller import BallRoller
from components.igus_slide import IgusSlide
from components.scam import Scam

#system imports
from systems.robot_system import RobotSystem

#Constants
CONTROL_LOOP_WAIT_TIME = .025
TRIGGER_THRESHOLD = .25

#Jag channels (PWM)
front_left_channel = 1
front_right_channel = 2
back_left_channel = 4
back_right_channel = 3
ball_roller_motor = 5

#Digital IO - TODO real values
ball_optical = 2
shuttle_optical = 1
led_spi_bus = 4
led_spi_clk = 5
compressor_switch = 6

#sensor channels analog
shuttle_mb10x3_port = 1
left_mb10x3_port = 2
right_mb10x3_port = 3

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

#Joystick channel
joystick_channel = 1

#PID configs taken from 2013 code, similar mechanism for control, needs to be tested
SCAM_P = -3000.0 
SCAM_I = -0.1 
SCAM_D = -14.0

#guess based on specs todo fix this based on emperical data
THRESHOLD = 2 #position in degrees
ANGLE_MAX_POSITION = 1
ANGLE_MIN_POSITION = .2
ANGLE_MIN_ANGLE = -15
ANGLE_MAX_ANGLE = 65



class MyRobot(wpilib.SimpleRobot):
    
    # keep in sync with driver station
    MODE_DISABLED       = 1
    MODE_AUTONOMOUS     = 2
    MODE_TELEOPERATED   = 3
    
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        
        #initilize all basic types( sensors, motors, stuuf like that)
        
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
        self.l_actuator.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Coast)
        self.l_actuator.SetPID(SCAM_P, SCAM_I, SCAM_D)
        
        self.l_actuator_auto = AnglePositionJaguar(self.l_actuator, THRESHOLD, ANGLE_MIN_POSITION, ANGLE_MAX_POSITION, ANGLE_MIN_ANGLE, ANGLE_MAX_ANGLE)
        
        
        #sensors
        self.shuttle_distance_sensor = GenericDistanceSensor(shuttle_mb10x3_port, MB10X3)
        self.left_distance_sensor = GenericDistanceSensor(left_mb10x3_port, MB10X3)
        self.right_distance_sensor = GenericDistanceSensor(right_mb10x3_port, MB10X3)
        
        ball_detector = wpilib.DigitalInput(ball_optical)
        shuttle_detector = wpilib.DigitalInput(shuttle_optical)
        self.ds = wpilib.DriverStation.GetInstance()
        self.sd = wpilib.SmartDashboard
        
        self.robot_drive = wpilib.RobotDrive(self.front_left_jag, self.back_left_jag, self.front_right_jag, self.back_right_jag)
        
        #create components
        self.ball_roller = BallRoller(ball_roller_relay)
        self.igus_slide  = IgusSlide(self.igus_motor, self.motor_release_solenoid, self.shuttle_distance_sensor, ball_detector, shuttle_detector)  
        self.scam = Scam(self.l_actuator_auto)
        self.components = [self.ball_roller, self.igus_slide, self.scam]
        
        #create systems
        self.robot_system = RobotSystem( self.scam, self.igus_slide, self.ball_roller)
        
        #storing modes for testing
        self.LOAD_MODE = LOAD_MODE
        self.PASS_MODE = PASS_MODE
        self.SHOOT_MODE = SHOOT_MODE
        
        #storing components for testing
        self.BallRoller = BallRoller
        self.Scam = Scam
        self.IgusSlide = IgusSlide
    def RobotInit(self):
        pass
        
    def Autonomous(self):        
        print("MyRobot::Autonomous()")
        
        while self.IsOperatorControl() and self.IsEnabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
    
    def OperatorControl(self):
        print("MyRobot::OperatorControl()")

        self.delay = PreciseDelay(CONTROL_LOOP_WAIT_TIME)

        # set the watch dog
        dog = self.GetWatchdog()
        dog.SetExpiration(0.25)
        dog.SetEnabled(True)

            
        while self.IsOperatorControl () and self.IsEnabled():
            dog.Feed()
            #
            #Drive
            #
            x_axis = self.logitech.GetX()
            y_axis = -self.logitech.GetY()
            twist = self.logitech.GetTwist()
            self.robot_drive.MecanumDrive_Cartesian(x_axis,y_axis, twist)
            
            #
            #robot_system modes
            #
            
            #these are exclusionary
            button_two = self.logitech.GetRawButton(2)
            l_trigger = self.logitech.GetRawButton(lt.L_TRIGGER)
            r_bumber = self.logitech.GetRawButton(lt.R_BUMPER)
            
            if button_two: #todo: find actual button
                self.robot_system.set_mode(LOAD_MODE)
                
            elif l_trigger: #todo: find actual button
                self.robot_system.set_mode(PASS_MODE)
                
            elif r_bumber: #todo: find actual button
                self.robot_system.set_mode(SHOOT_MODE)

            #
            #actions
            #
            
            #most of these can be done at the same time 
            if self.logitech.GetRawButton(lt.R_BUMPER):
                self.robot_system.move_scam(self.logitech.GetRawAxis(lt.R_AXIS_Y))
            

            #
            # mode based action
            #
            
            #it makes sense for some buttons to have diffrent functions in diffrent modes
            if self.logitech.GetRawButton(lt.R_TRIGGER):
                if self.robot_system.get_mode() == PASS_MODE:
                    
                    #in this case this should pass the ball out of the robot
                    self.robot_system.ball_roll(OUT)
                        
                    
                elif self.robot_system.get_mode() == SHOOT_MODE:
                    
                    self.robot_system.shoot()
                    
            #sr todo: figure out the rest of the controls
            
            
            
            #do all the robot actions
            self.robot_system.do_auto_actions()
            
            
            #update components, has to be the last thing called except wait
            self.update()
            
            
            self.delay.wait()
                        
            
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
    