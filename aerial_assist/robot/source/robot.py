try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#common imports
from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3
from common.ez_can_jaguar import EzCanJaguar


#component imports
from components.ball_roller import BallRoller
from components.igus_slide import IgusSlide

#system imports
from systems.scam import Scam

#Constants
CONTROL_LOOP_WAIT_TIME = .025
TRIGGER_THRESHOLD = .25

#Jag channels (PWM)
front_left_channel = 1
front_right_channel = 2
back_left_channel = 3
back_right_channel = 4
ball_roller_motor = 5

#Digital IO - TODO real values
shuttle_limit = 1
ball_optical = 2
shuttle_optical = 3
led_spi_bus = 4
led_spi_clk = 5
pressureSwitchChannel = 6

#sensor channels analog
mb10x3_port = 1

#CAN channels (probably not 5 and 6)
winch_can = 5
scam_motor_can = 6

#solenoid channels
solenoid1 = 1
solenoid2 = 2

#relay channels
compressorRelayChannel = 1
camera_led_relay = 2
ball_roller_relay = 3

#Joystick channel
joystick_channel = 1

#Drive jags
front_left_jag =  wpilib.Jaguar(front_left_channel)
front_right_jag = wpilib.Jaguar(front_right_channel)
back_left_jag =   wpilib.Jaguar(back_left_channel)
back_right_jag =  wpilib.Jaguar(back_right_channel)

#CAN jags
#winch is operated on percent vbus no extra setup is needed
winch_jag = EzCanJaguar(winch_can)

#PID configs taken from 2013 code, similar mechanism for control, needs to be tested
SCAM_P = -3000.0 
SCAM_I = -0.1 
SCAM_D = -14.0

#guess based on specs todo fix this based on emperical data
ANGLE_MAX_POSITION = .7
ANGLE_MIN_POSITION = 0
ANGLE_MIN_ANGLE = -15
ANGLE_MAX_ANGLE = 65

scam_motor = EzCanJaguar(scam_motor_can)
scam_motor.SetPositionReference(wpilib.CANJaguar.kPosRef_Potentiometer)
#guess on number of turns, but it should be treated as one turn anyway
scam_motor.ConfigPotentiometerTurns(1)
scam_motor.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Coast)
scam_motor.SetPID(SCAM_P, SCAM_I, SCAM_D)

#DoubleSolenoid config 
double_solenoid = wpilib.DoubleSolenoid(solenoid1, solenoid2)

#Compressor
compressor = wpilib.Compressor(pressureSwitchChannel, compressorRelayChannel)

# relay
camera_led = wpilib.Relay(camera_led_relay)
camera_led.Set(wpilib.Relay.kForward)

ball_roller_relay = wpilib.Relay(b)
#Joystick
joystick = wpilib.Joystick(joystick_channel)

#sensors
shuttle_distance_sensor = GenericDistanceSensor(shuttle_optical)
ball_detector = wpilib.DigitalInput(ball_optical)
shuttle_detector = wpilib.DigitalInput(shuttle_optical)


class MyRobot(wpilib.SimpleRobot):
    
    # keep in sync with driver station
    MODE_DISABLED       = 1
    MODE_AUTONOMOUS     = 2
    MODE_TELEOPERATED   = 3
    
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        
        self.ds = wpilib.DriverStation.GetInstance()
        robot_drive = wpilib.RobotDrive(front_left_jag, back_left_jag, front_right_jag, back_right_jag)

        #create components
        ball_roller = BallRoller()
        
        

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
            
            #
            #Drive
            #
            x_axis = joystick.GetX()
            y_axis = joystick.GetY()
            twist = joystick.GetTwist()
            self.robot_drive.MecanumDrive_Polar(y_axis, x_axis, twist)
            
            #
            #Scam modes
            #
            
            #what happens if I click all of these?
            
            if joystick.GetRawButton(1): #todo: find actual button
                scam.load_mode()
                
            if joystick.GetRawButton(2): #todo: find actual button
                scam.pass_mode()
                
            if joystick.GetRawButton(3): #todo: find actual button
                scam.shoot_mode()
                
            if joystick.GetTrigger() > TRIGGER_THRESHOLD:
                igus_slide.shoot()
            #
            #Manual over ride
            #
            
            #what is this what do you mean, GetTrigger gets a bool no a value
            #also, if let go of the button then I will just go into the other modes
            if joystick.GetTrigger() < TRIGGER_THRESHOLD * -1:
                right_y_axis = joystick.GetZ() #todo: find the actual function
                scam.set_scam(right_y_axis)
            
            if joystick.GetRawButton(6): #todo: find actual button
                igus_slide.retract()
                
            if joystick.GetRawButton(5): #todo: find actual button
                ball_roller.ball_roller.set(ball_roller.OUT)
def run():
    
    # this is initialized in StartCompetition, but one of our
    # constructors might use it, and crash
    wpilib.SmartDashboard.init()
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot

if __name__ == '__main__':
    wpilib.run()