try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from delay import PreciseDelay

joystick = wpilib.Joystick(1)
shuttle_motor_channel = 2
l_actuator_channel = 1
valve1_channel = 2
valve2_channel = 1
compressor_relay = 1
compressor_switch = 5
compressor = wpilib.Compressor(compressor_switch, compressor_relay)
shuttle_motor = wpilib.Jaguar(shuttle_motor_channel)
l_actuator = wpilib.Jaguar(l_actuator_channel)
valve1 = wpilib.Solenoid(valve1_channel)
valve2 = wpilib.Solenoid(valve2_channel)
CONTROL_LOOP_WAIT_TIME = 0.025
next_state = None
current_state = None


class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)

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
                l_actuator.Set(0)
                    
            if joystick.GetRawButton(11):
                next_state = CLIMB
                
            elif joystick.GetRawButton(10):
                next_state = LOWER
                
            
            if next_state is not None and next_state != current_state:
                
                current_state = next_state
                next_state = None
        
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