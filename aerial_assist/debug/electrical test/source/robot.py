try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


from common.delay import PreciseDelay
from common.generic_distance_sensor import GenericDistanceSensor, MB10X3

#XBOX CONTROLLER SETUP
XBOX_A = 1
XBOX_B = 2
XBOX_X = 3
XBOX_Y = 4
XBOX_LBUMPER = 5
XBOX_RBUMPER = 6
XBOX_SELECT = 7
XBOX_START = 8
XBOX_LEFTA_BUTTON = 9
XBORX_RIGHTA_BUTTON = 10
#ZAXIS is controlled but the two triggers
#AXIS 4 and 5 are Right axis 
#D_PAD IS CONTROLLED BY axis 6
#axises
XBOX_LEFTX  = 1
XBOX_LEFTY = 2
XBOX_RIGHTX = 3
XBOX_RIGHTY = 4
XBOX_TRIGGER = 5 #left is - right is +
XBOX_DPAD =   6  #only x axis works and is 1 or -1

#digital I/O
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



#can channels
shuttle_motor_channel = 1
l_actuator_channel = 2

#solenoids
valve1_channel = 1
valve2_channel = 2

#Relay
compressor_relay = 7
ball_roller_relay_port = 5




CONTROL_LOOP_WAIT_TIME = 0.025
next_state = None
current_state = None





class MyRobot(wpilib.SimpleRobot):
    def __init__(self):
        wpilib.SimpleRobot.__init__(self)
        
        #PWM
        self.front_left_jag =  wpilib.Jaguar(1)
        self.front_right_jag = wpilib.Jaguar(2)
        self.back_left_jag =   wpilib.Jaguar(4)
        self.back_right_jag =  wpilib.Jaguar(3)

        self.robot_drive = wpilib.RobotDrive(self.front_left_jag, self.back_left_jag, self.front_right_jag, self.back_right_jag)
        self.sd = wpilib.SmartDashboard
        
        self.ball_detector = wpilib.DigitalInput(ball_optical)
        self.shuttle_detector = wpilib.DigitalInput(shuttle_optical)
        
        self.shuttle_dist = GenericDistanceSensor(shuttle_distance_sensor, MB10X3)
        self.front_dist_left = GenericDistanceSensor(left_distance_sensor, MB10X3)
        self.front_dist_right = GenericDistanceSensor(right_distance_sensor, MB10X3)
        
        self.ball_roller_relay = wpilib.Relay(ball_roller_relay_port)
        self.shooter_solenoid = wpilib.DoubleSolenoid(valve1_channel, valve2_channel)
        
        self.compressor = wpilib.Compressor(compressor_switch, compressor_relay)
        self.shuttle_motor = wpilib.CANJaguar(shuttle_motor_channel, wpilib.CANJaguar.kPercentVbus)
        self.shuttle_motor.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Brake)
        
        #l_actuator currently a vbus
        self.l_actuator = wpilib.CANJaguar(l_actuator_channel, wpilib.CANJaguar.kPercentVbus)
        
        self.l_actuator.SetPositionReference(wpilib.CANJaguar.kPosRef_Potentiometer)
        self.l_actuator.ConfigPotentiometerTurns(1)
        self.l_actuator.ConfigNeutralMode(wpilib.CANJaguar.kNeutralMode_Brake)
        #l_actuator.SetPID(-3000.0, -0.1, -14.0)
        
        self.joystick = wpilib.Joystick(1)
    def RobotInit(self):
        pass

    def Disabled(self):
        print("MyRobot::Disabled()")
        while self.IsDisabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
            
    def Autonomous(self):
        print("MyRobot::Autonomous()")
        
        while self.IsAutonomous() and self.IsEnabled():
            wpilib.Wait(CONTROL_LOOP_WAIT_TIME)
            
    def OperatorControl(self):
        print("MyRobot::Enabled")
        delay = PreciseDelay(CONTROL_LOOP_WAIT_TIME)
        CLIMB = 0
        LOWER = 1
        self.compressor.Start()
        wd = self.watchdog
        wd.SetExpiration(CONTROL_LOOP_WAIT_TIME * 2)
        wd.SetEnabled(True)
        while self.IsOperatorControl() and self.IsEnabled():
            wd.Feed()
            y_axis = self.joystick.GetX()
            x_axis = -self.joystick.GetY()
            twist = self.joystick.GetRawAxis(4)
            self.robot_drive.MecanumDrive_Cartesian(x_axis, y_axis, twist)
            
            if self.joystick.GetRawButton(XBOX_A):
                self.shuttle_motor.Set(-.8)
            else:
                self.shuttle_motor.Set(0)
            
            if self.joystick.GetRawButton(XBOX_X):
                print("l_actuator -1")
                self.l_actuator.Set(-1)
            elif self.joystick.GetRawButton(XBOX_B):
                print("l_actuator 1")
                self.l_actuator.Set(1) 
            else:
                self.l_actuator.Set(0)
                
            self.sd.PutNumber("Actuator pot:", self.l_actuator.GetPosition())

                
            #xbox axis left and right on dpad 
            if joystick.GetRawButton(XBOX_START):   
                print(" relay set to 1")
                self.ball_roller_relay.Set(wpilib.Relay.kForward)
            elif joystick.GetRawButton(XBOX_SELECT):
                print( "relay set to -1")
                self.ball_roller_relay.Set(wpilib.Relay.kReverse)
            else:
                self.ball_roller_relay.Set(0)
                
            self.sd.PutNumber("Ball roller", int(self.joystick.GetRawAxis(6)))
                
            
            if joystick.GetRawButton(XBOX_LBUMPER):
                print('kForward')
                self.shooter_solenoid.Set(wpilib.DoubleSolenoid.kForward)
                
            elif joystick.GetRawButton(XBOX_RBUMPER):
                print('kReverse')
                self.shooter_solenoid.Set(wpilib.DoubleSolenoid.kReverse)
                
        

            self.sd.PutBoolean("Shuttle detector", bool(self.shuttle_detector.Get()))
        

            self.sd.PutBoolean("Ball detector", bool(self.ball_detector.Get()))
        
            
            self.sd.PutNumber("Shuttle Distance", self.shuttle_dist.GetDistance())
            self.sd.PutNumber("Front distance left", self.front_dist_left.GetDistance())
            self.sd.PutNumber("Front distance right", self.front_dist_right.GetDistance())
            
            self.sd.PutBoolean("l_actuator FL", self.l_actuator.GetForwardLimitOK())
            self.sd.PutBoolean("l_actuator RL", self.l_actuator.GetReverseLimitOK())
            self.sd.PutBoolean("shuttle_motor FL", self.shuttle_motor.GetForwardLimitOK())
            self.sd.PutBoolean("shuttle_motor RL", self.shuttle_motor.GetReverseLimitOK())
            
            
            # idle state: don't engage either solenoid
            delay.wait()
        self.compressor.Stop()
        
def run():
    
    # this is initialized in StartCompetition, but one of our
    # constructors might use it, and crash
    wpilib.SmartDashboard.init()
    
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot

if __name__ == '__main__':
    wpilib.run()
        