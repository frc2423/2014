try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3


shuttle_limit = 1
ball_optical = 2
shuttle_optical = 3
joystick = wpilib.Joystick(1)
shuttle_motor_channel = 1
l_actuator_channel = 2
valve1_channel = 2
valve2_channel = 1
compressor_relay = 1
compressor_switch = 2
compressor = wpilib.Compressor(compressor_switch, compressor_relay)
shuttle_motor = wpilib.CANJaguar(shuttle_motor_channel, wpilib.CANJaguar.kPercentVbus)
shuttle_motor.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Coast)
l_actuator = wpilib.CANJaguar(l_actuator_channel, wpilib.CANJaguar.kPercentVbus)
l_actuator.SetPositionReference(wpilib.CANJaguar.kPosRef_Potentiometer)
l_actuator.ConfigPotentiatorTurns(1)
l_actuator.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Coast)
l_actuator.SetPID(-3000.0, -0.1, -14.0)
ball_roller_relay = wpilib.Relay(2)
valve1 = wpilib.Solenoid(valve1_channel)
valve2 = wpilib.Solenoid(valve2_channel)
CONTROL_LOOP_WAIT_TIME = 0.025
next_state = None
current_state = None
front_left_jag =  wpilib.Jaguar(5)
front_right_jag = wpilib.Jaguar(6)
back_left_jag =   wpilib.Jaguar(3)
back_right_jag =  wpilib.Jaguar(4)
shuttle_distance_sensor = GenericDistanceSensor(shuttle_optical)
ball_detector = wpilib.DigitalInput(ball_optical)
shuttle_detector = wpilib.DigitalInput(shuttle_optical)
shuttle_dist = GenericDistanceSensor(1)
front_dist_one = GenericDistanceSensor(2)
front_dist_two = GenericDistanceSensor(3)

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
                next_state = CLIMB
                
            elif joystick.GetRawButton(10):
                next_state = LOWER
                
            
            if next_state is not None and next_state != current_state:
                
                current_state = next_state
                next_state = None
        
            if not shuttle_detector:
                self.sd.PutBoolean("Shuttle detector", True)
        
            if shuttle_detector:
                self.sd.PutBoolean("Shuttle detector", False)
            
            if not ball_detector:
                self.sd.PutBoolean("Ball detector", True)
        
            if ball_detector:
                self.sd.PutBoolean("Ball detector", False)
            
            if not shuttle_optical:
                self.sd.PutBoolean("Shuttle optical", True)
        
            if shuttle_optical:
                self.sd.PutBoolean("Shuttle optical", False)
            
            self.sd.PutNumber("Shuttle Distance", shuttle_dist.GetDistance())
            self.sd.PutNumber("Front distance one", front_dist_two.GetDistance())
            self.sd.PutNumber("Front distance two", front_dist_one.GetDistance())
        
            # idle state: don't engage either solenoid
            if current_state is None:
                
                valve1.Set(False)
                valve2.Set(False)
                else:
        
            if current_state == CLIMB:
                valve1.Set(False)
                    
                valve2.Set(True)
            else:
                valve1.Set(True)
                    
                valve2.Set(False)
            delay.wait()
        compressor.Stop()
        
def run():
    
    # this is initialized in StartCompetition, but one of our
    # constructors might use it, and crash
    wpilib.SmartDashboard.init()
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot