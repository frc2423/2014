try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#common imports
from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3, GP2D120
from common.ez_can_jaguar import EzCANJaguar 
from common.auto_jaguar import AnglePositionJaguar
from common.modes import *
import common.logitech_controller as lt

#component imports
from components.ball_roller import BallRoller
import components.ball_roller as bl
from components.igus_slide import IgusSlide
from components.scam import Scam

#system imports
from systems.robot_system import RobotSystem

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
shuttle_optical =5

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
SCAM_P = 3000
SCAM_I = .1
SCAM_D = 14

#guess based on specs todo fix this based on emperical data
THRESHOLD = .02 #position in degrees
ANGLE_MAX_POSITION = .757
ANGLE_MIN_POSITION = .042
ANGLE_MIN_ANGLE = 65
ANGLE_MAX_ANGLE = -30



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
        
        self.ball_detector = GenericDistanceSensor(ball_optical, GP2D120)
        self.shuttle_detector = GenericDistanceSensor(shuttle_optical, GP2D120)
        
        self.ds = wpilib.DriverStation.GetInstance()
        self.sd = wpilib.SmartDashboard
        
        self.robot_drive = wpilib.RobotDrive(self.front_left_jag, self.back_left_jag, self.front_right_jag, self.back_right_jag)
        
        #create components
        self.ball_roller = BallRoller(ball_roller_relay)
        self.igus_slide  = IgusSlide(self.igus_motor, self.motor_release_solenoid, self.shuttle_distance_sensor, self.ball_detector, self.shuttle_detector)  
        self.scam = Scam(self.l_actuator_auto)
        
        #create systems
        self.robot_system = RobotSystem( self.scam, self.igus_slide, self.ball_roller)
        
                # autonomous mode needs a dict of components
        components = {
            # components 
            'ball_roller': self.ball_roller,
            'igus_slide': self.self.igus_slide,
            'scam': self.scam, 
            
            # systems
            'robot_system': self.robot_system,
        }
        
        self.components = []
        self.components = [v for v in components.values() if hasattr(v, 'update')]
        
        #
        #determines if we are to automatically switch states from loading to shooting
        #
        
        self.auto_load = True
        
        #self.operator_control_mode = OperatorControlManager(components, self.ds)
    def RobotInit(self):
        pass
        
    def Disabled(self):
        print("MyRobot::Disabled()")
        
        self.sd.PutNumber("Robot Mode", self.MODE_DISABLED)
    
        while self.IsDisabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
            
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
        
        next_mode = None
            
        while self.IsOperatorControl () and self.IsEnabled():
            dog.Feed()
            #
            #Drive
            #
            y_axis = self.logitech.GetRawAxis(lt.L_AXIS_Y)
            twist =  self.logitech.GetRawAxis(lt.R_AXIS_X)
            x_axis = self.logitech.GetRawAxis(lt.L_AXIS_X)
 
            axes = [y_axis, twist, x_axis]
            for axis in axes: 
                if axis < .1:
                    axis = 0
                    
            self.robot_drive.MecanumDrive_Cartesian(x_axis, y_axis, twist )
        
            #
            #robot_system modes
            #
            
            #
            #these are exclusionary, change the mode based on user input
            #if no user input check if there is a next mode and set to it
            #if there is
            #
            if self.logitech.GetRawButton(1): #todo: find actual button
                self.mode = LOAD_MODE
                next_mode = None
                
            elif self.logitech.GetRawButton(2): #todo: find actual button
                self.mode = PASS_MODE
                next_mode = None
                
            elif self.logitech.GetRawButton(3): #todo: find actual button
                self.mode =SHOOT_MODE
                next_mode = None
            
            elif self.next_mode != None:
                #
                #after setting the next mode, clear it so we dont get confused
                #
                self.mode = next_mode
                self.next_mode = None
                

            #
            #LOAD_MODE actions
            #
            
            if self.mode == LOAD_MODE:
                #switch between if we can auto load or not
                if self.logitech.GetRawButton(4):
                    self.auto_load = not self.auto_load
                
                #
                #Auto feed the ball
                #
                self.ball_roller.roll_in()
                
                #
                # Set the position of the scam first do angle control, set to 0
                # if we are already in the goal range
                #
                
                self.scam.set_angle(self.scam.LOADING_ANGLE)
                
                # we are in position, stop using PID, were better without it
                if self.scam.in_position():
                    self.scam.set_speed(0)
                    
                #put igus into loading mode    
                self.igus_slide.retract_load()
                
                #if auto load is active set our next mode
                if(self.auto_load):
                    if (self.igus_slide.ball_sensor_triggered):
                        next_mode = SHOOT_MODE
                        
                        
            #
            #SHOOT_MODE actions
            #
            if self.mode == SHOOT_MODE:
                
                #
                #while we are not in position the ball rollers should keep feeding
                #the ball in
                #
                
                self.ball_roller.roll_in()
                #
                # Set the position of the scam first do angle control, set to 0
                # if we are already in the goal range
                #
                
                self.scam.set_angle(self.scam.SHOOTING_ANGLE)
                
                # we are in position, stop using PID, were better without it
                if self.scam.in_position():
                    self.scam.set_speed(0)
                    #we are in position ball rollers don't need to be rolled in
                    #any more
                    self.ball_roller.off()
                    
                #
                #Retract to shooting position, if we are not already there
                #
                self.igus_slide.retract_shoot()
                
                
                #
                #shoot if trigger is hit, user can shoot at any point by pressing both triggers
                #igus_slide will automatically try to shoot
                #
                
                if self.logitech.GetRawButton(lt.R_TRIGGER):
                    self.igus_slide.shoot(override = self.logitech.GetRawButton(lt.L_TRIGGER))
                
            
            #
            #PASS_MODE actions
            #
            if self.mode  == PASS_MODE:
                #switch between if we can auto load or not
                if self.logitech.GetRawButton(4):
                    self.auto_load = not self.auto_load
                
                #
                #Pass the ball by user command
                #
                if self.logitech.GetRawButton(lt.R_BUMMPER):
                    self.ball_roller.roll_out()
                

                #
                # Set the position of the scam first do angle control, set to 0
                # if we are already in the goal range
                #
                
                self.scam.set_angle(self.scam.LOADING_ANGLE)
                
                # we are in position, stop using PID, were better without it
                if self.scam.in_position():
                    self.scam.set_speed(0)
                    
            
            #update smartdashboard
                self.sd.PutString("Robot Mode", mode_dict[self.mode])
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
    