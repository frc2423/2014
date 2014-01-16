try:
    import wpilib
except ImportError:
    from pyfrc import wpilib
#Jag channels
front_left_channel = 1
front_right_channel = 2
back_left_channel = 3
back_right_channel = 4
#Drive jags
front_left_jag = wpilib.Jaguar(front_left_channel)
front_right_jag = wpilib.Jaguar(front_right_channel)
back_left_jag = wpilib.Jaguar(back_left_channel)
back_right_jag = wpilib.Jaguar(back_right_channel)

#Joystick channel
joystick_one_channel

#Joystick
joystick = wpilib.Joystick(joystick_one_channel)

CONTROL_LOOP_WAIT_TIME = .025

class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        
        self.ds = wpilib.DriverStation.GetInstance()
        self.robot_drive = wpilib.RobotDrive(front_left_jag, back_left_jag, front_right)jag, back_right_jag)
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
            
            self.robot_drive.MecanumDrive_Cartesian(y_axis, x_axis, 
if __name__ == '__main__':
    wpilib.run()