try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3

#digital I/Oop
ball_optical = 2
shuttle_optical = 1
light_data = 4
light_clock = 5
compressor_switch = 6

#analog
left_distance_sensor = 2
right_distance_sensor = 3
shuttle_distance_sensor = 1

#joystick
joystick = wpilib.Joystick(1)

#PWM
front_left_jag =  wpilib.Jaguar(5)
front_right_jag = wpilib.Jaguar(6)
back_left_jag =   wpilib.Jaguar(4)
back_right_jag =  wpilib.Jaguar(3)

#can channels
shuttle_motor_channel = 1
l_actuator_channel = 2

#solenoids
valve1_channel = 1
valve2_channel = 2

#Relay
compressor_relay = 1
ball_roller_relay = 2

compressor = wpilib.Compressor(compressor_switch, compressor_relay)
shuttle_motor = wpilib.CANJaguar(shuttle_motor_channel, wpilib.CANJaguar.kPercentVbus)
shuttle_motor.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Coast)

#l_actuator currently a vbus
l_actuator = wpilib.CANJaguar(l_actuator_channel, wpilib.CANJaguar.kPercentVbus)

#l_actuator.SetPositionReference(wpilib.CANJaguar.kPosRef_Potentiometer)
#l_actuator.ConfigPotentiatorTurns(1)
#l_actuator.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Coast)
#l_actuator.SetPID(-3000.0, -0.1, -14.0)

ball_roller_relay = wpilib.Relay(ball_roller_relay)
shooter_solenoid = wpilib.DoubleSolenoid(valve1_channel, valve2_channel)

CONTROL_LOOP_WAIT_TIME = 0.025
next_state = None
current_state = None


ball_detector = wpilib.DigitalInput(ball_optical)
shuttle_detector = wpilib.DigitalInput(shuttle_optical)

shuttle_dist = GenericDistanceSensor(shuttle_distance_sensor, MB10X3)
front_dist_left = GenericDistanceSensor(left_distance_sensor, MB10X3)
front_dist_right = GenericDistanceSensor(right_distance_sensor, MB10X3)

class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        robot_drive = wpilib.RobotDrive(front_left_jag, back_left_jag, front_right_jag, back_right_jag)
        self.sd = wpilib.SmartDashboard
        
    def RobotInit(self):
        pass

    def Disabled(self):
        print("MyRobot::Disabled()")
        while self.IsDisabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
            
    def Autonomous(self):
        print("MyRobot::Autonomous()")
        
        while self.IsOperatorControl() and self.IsEnabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
            
    def OperatorControl(self):
        print("MyRobot::Enabled")
        global next_state
        global current_state
        global valve1
        global valve2
        delay = PreciseDelay(CONTROL_LOOP_WAIT_TIME)
        wpilib
        CLIMB = 0
        LOWER = 1
        compressor.Start()
        while self.IsOperatorControl () and self.IsEnabled():
            
            x_axis = joystick.GetX()
            y_axis = joystick.GetY()
            twist = joystick.GetTwist()
            self.robot_drive.MecanumDrive_Polar(y_axis, x_axis, twist)
            
            if joystick.GetRawButton(8):
                shuttle_motor.Set(.8)
            elif joystick.GetRawButton(9):
                shuttle_motor.Set(-.8)
            else:
                    shuttle_motor.Set(0)
            
            if joystick.GetRawButton(6):
                l_actuator.Set(.8)
                
            elif joystick.GetRawButton(7):
                l_actuator.Set(-.8)
                
            else:
                ball_roller_relay.Set(0)
                
            self.sd.PutNumber("Actuator pot:", l_actuator.Get_Position)

            
                
                
            if joystick.GetRawButton(4):
                ball_roller_relay.Set(1)
                ball_status = "forward"
                
            elif joystick.GetRawButton(5):
                ball_roller_relay.Set(-1)
                ball_status = "backward"
            else:
                ball_roller_relay.Set(0)
                ball_status = "off"
                
            self.sd.PutString("Ball roller status:", ball_status)
                
            
            if joystick.GetRawButton(11):
                shooter_solenoid.Set(wpilib.DoubleSolenoid.kForward)
                
            elif joystick.GetRawButton(10):
                shooter_solenoid.Set(wpilib.DoubleSolenoid.kReverse)
                
            
            if next_state is not None and next_state != current_state:
                
                current_state = next_state
                next_state = None
        

            self.sd.PutBoolean("Shuttle detector", shuttle_detector.Get())
        

            self.sd.PutBoolean("Ball detector", ball_detector.Get())
            

            self.sd.PutBoolean("Shuttle optical", shuttle_optical.Get())
        
            
            self.sd.PutNumber("Shuttle Distance", shuttle_dist.GetDistance())
            self.sd.PutNumber("Front distance left", front_dist_left.GetDistance())
            self.sd.PutNumber("Front distance right", front_dist_right.GetDistance())
        
            # idle state: don't engage either solenoid
            delay.wait()
        compressor.Stop()
        
def run():
    
    # this is initialized in StartCompetition, but one of our
    # constructors might use it, and crash
    wpilib.SmartDashboard.init()
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot