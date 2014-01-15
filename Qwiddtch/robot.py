try:
    import wpilib 
except ImportError:
    import fake_wpilib as wpilib

#
#Import all systems and components here
#
from components.angle import Angle
from components.feeder import Feeder
from components.shooter import Shooter
  

from common.ez_can_jaguar import EzCANJaguar
from common.delay import PreciseDelay
#
#Declare constants
#

ANGLE_CONTROLLER_SPEED = .5

# control loop time
# used to guarantee that our control loop takes a certain time
CONTROL_LOOP_WAIT_TIME = 0.025

#
#Declare all the ports and channels here
#Note: these are shared between the electrical test and main code!
#




#CAN channels
shooter_wheel_can = 1
angle_control_can = 2

#Jaguar channels
left_drive_PWM = 1
right_drive_PWM = 2
feeder_servo_PWM = 3

#Joystick Channels
joystick_channel_one = 1

#Joysticks
joystick = wpilib.Joystick(joystick_channel_one)

#
#Create motors/sensors here
#

shooter_wheel = EzCANJaguar(shooter_wheel_can)

angle_control = EzCANJaguar(angle_control_can)

feeder_servo = wpilib.Servo(feeder_servo_PWM)

l_drive = wpilib.Jaguar(left_drive_PWM)

r_drive = wpilib.Jaguar(right_drive_PWM)



class MyRobot (wpilib.SimpleRobot):
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        
            
        
        
        #create component instances
        '''ex self.my_feeder = Feeder(feeder_motor, 
        frisbee_sensor, 
        feeder_sensor)'''
        self.feeder = Feeder(feeder_servo)
        self.angle = Angle(angle_control)
        self.shooter = Shooter(shooter_wheel)
        self.robot_drive = wpilib.RobotDrive(l_drive, r_drive)
        
        
        
        
        
        #In the 2013 code we had a dictionary of autonomous mode components. I'm assuming we are keeping that.
        
        
        #initialize other needed SmartDashboard imputs if we use it. This would be real competition stuff.
        
        
    def RobotInit(self):
        pass
    
    def Disabled(self):
        print("MyRobot::Autonomous()")
        
        while self.IsDisabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
        
        
    def Autonomous(self):        
        print("MyRobot::Autonomous()")
        
        while self.IsOperatorControl() and self.IsEnabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
        #self.sd.PutNumber("Robot Mode", self.MODE_AUTONOMOUS)

        
    def OperatorControl(self):
        print("MyRobot::OperatorControl()")

        self.delay = PreciseDelay(CONTROL_LOOP_WAIT_TIME)

        # set the watch dog
        dog = self.GetWatchdog()
        dog.SetExpiration(0.25)
        dog.SetEnabled(True)

            
        while self.IsOperatorControl () and self.IsEnabled():
            
            #
            #angle
            #
            if joystick.GetRawButton(3):
                self.angle.set_speed(ANGLE_CONTROLLER_SPEED)
            elif joystick.GetRawButton(2):
                self.angle.set_speed(-ANGLE_CONTROLLER_SPEED)
            
            #
            #shooter
            #
            # gets the value of the throttle treating -1 as 0
            self.d_speed = (joystick.GetThrottle() + 1) / 2
            self.shooter.set_speed(self.d_speed)
    
            #
            #feeder
            #
            if joystick.GetTrigger():
                self.feeder.feed()
                
            #
            #update everything
            #    
            self.angle.update()
            self.feeder.update()
            self.shooter.update()
            
            #
            #Set the drive
            #
            self.robot_drive.ArcadeDrive(joystick.GetY(), joystick.GetX(), True)
            

            dog.Feed()
            
            self.delay.wait()
        
def run():
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot


