import wpilib

from delay import PreciseDelay


relay = wpilib.Relay(2, 8)
joystick = wpilib.Joystick(1)
valve1_channel = 2
valve2_channel = 1
compressor_relay = 1
compressor_switch = 5
compressor = wpilib.Compressor(compressor_switch, compressor_relay)
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
            
            if joystick.GetRawButton(7):
                relay.Set(1)
                
            if joystick.GetRawButton(8):
                relay.set(0)
            
            if joystick.GetTrigger():
                compressor.Start()
                
            if joystick.GetRawButton(2):
                compressor.Stop()
            
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
    
    return robots