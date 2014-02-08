try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from common.delay import PreciseDelay
from systems.scam import scam
from components import ball_roller
from components.igus_slide import igus_slide

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

#Compressor channels
compressorRelayChannel = 0
pressureSwitchChannel = 1

#Compressor
compressor = wpilib.Compressor(pressureSwitchChannel, compressorRelayChannel)

#Joystick channel
joystick_channel = 1

#Joystick
joystick = wpilib.Joystick(joystick_channel)

#Constants
CONTROL_LOOP_WAIT_TIME = .025
TRIGGER_THRESHOLD = .25

class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        
        self.ds = wpilib.DriverStation.GetInstance()
        robot_drive = wpilib.RobotDrive(front_left_jag, back_left_jag, front_right_jag, back_right_jag)
        self.robot_drive = robot_drive
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