try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from delay import PreciseDelay

joystick = wpilib.Joystick(1)
motor1_channel = 1
motor2_channel = 2
valve1_channel = 2
valve2_channel = 1
compressor_relay = 1
compressor_switch = 5
compressor = wpilib.Compressor(compressor_switch, compressor_relay)
motor1 = wpilib.CANJaguar(motor1_channel, kPercentVbus)
motor2 = wpilib.CANJaguar(motor2_channel, kPercentVbus)
valve1 = wpilib.Solenoid(valve1_channel)
valve2 = wpilib.Solenoid(valve2_channel)
control_loop_wait_time = 0.025
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
            wpilib.Wait(control_loop_wait_time)
            
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
        delay = PreciseDelay(control_loop_wait_time)
        wpilib
        CLIMB = 0
        LOWER = 1
        compressor.Start()
        while self.IsOperatorControl () and self.IsEnabled():
            
            zaxis = joystick.GetZ()
            motor1.Set(zaxis, 0)
            
            if joystick.GetRawButton(1)
                motor2.Set(.8, 0)
                
            if joystick.GetRawButton(2)
                motor2.Set(-.8, 0)
            
            if joystick.GetRawButton(11):
                next_state = CLIMB
                print("test")
            if joystick.GetRawButton(10):
                next_state = LOWER
                print("test2")
            if next_state is not None and next_state != current_state:
                print("test3")
                current_state = next_state
                next_state = None
        
        # idle state: don't engage either solenoid
            if current_state is None:
                print("test4")
                valve1.Set(False)
                valve2.Set(False)
            else:
        
                if current_state == CLIMB:
                    valve1.Set(False)
                    print("test5")
                    valve2.Set(True)
                else:
                    valve1.Set(True)
                    print("test6")
                    valve2.Set(False)
            delay.wait()
        compressor.Stop()
        
def run():
    
    # this is initialized in StartCompetition, but one of our
    # constructors might use it, and crash
    wpilib.SmartDashboard.init()
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robots