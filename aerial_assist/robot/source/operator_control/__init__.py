'''
    Implements an operator control mode management program. Example usage:
    
        from manual import OperatorControlManager
        
        components = {'drive': drive, 
                      'component1': component1, ... }
        ds = wpilib.DriverStation.GetInstance()
        operator_control = OperatorControlManager(components, robot_drive, ds)
        
        class MyRobot(wpilib.SimpleRobot):
        
            ... 
            
            def OperatorControl(self):
                operatorcontrol.run(self, control_loop_wait_time)
                
            def update(self):
            
                ... 
    
    Note that the robot instance passed to OperatorControlManager.run() must
    have an update function. 
'''

from glob import glob
import imp
import inspect
import os
import sys

from common.delay import PreciseDelay
from common.logitech_util import *
from common.logitech_controller import *

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib


class OperatorControlManager(object):
    '''
        The operator  manager loads all operator  mode modules and allows
        the user to select one of them via the SmartDashboard. 
        
        See template.txt for a sample operator  mode module
    '''
    
    def __init__(self, components, robot_drive, ds):
        
        self.ds = wpilib.DriverStation.GetInstance()
        self.modes = {}
        self.active_mode = None
        self.robot_drive = robot_drive
        print( "OperatorControlManager::__init__() Begins" )
        
        # load all modules in the current directory
        modules_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(modules_path)
        modules = glob(os.path.join(modules_path, '*.py' ))
        
        for module_filename in modules:
            
            module_name = os.path.basename(module_filename[:-3])
            
            if module_name in  ['__init__', 'manager']:
                continue
        
            try:
                module = imp.load_source(module_name, module_filename)
            except:
                if not self.ds.IsFMSAttached():
                    raise
            
            #
            # Find operator control mode classes in the modules that are present
            # -> note that we actually create the instance of the objects here,
            #    so that way we find out about any errors *before* we get out 
            #    on the field.. 
            
            for name, obj in inspect.getmembers(module, inspect.isclass):

                if hasattr(obj, 'MODE_NAME') :
                    try:
                        instance = obj(components, ds)
                    except:
                        
                        if not self.ds.IsFMSAttached():
                            raise
                        else:
                            continue
                    
                    if instance.MODE_NAME in self.modes:
                        if not self.ds.IsFMSAttached():
                            raise RuntimeError( "Duplicate name %s in %s" % (instance.MODE_NAME, module_filename) )
                        
                        print( "ERROR: Duplicate name %s specified by object type %s in module %s" % (instance.MODE_NAME, name, module_filename))
                        self.modes[name + '_' + module_filename] = instance
                    else:
                        self.modes[instance.MODE_NAME] = instance
        
        # now that we have a bunch of valid operator  mode objects, let 
        # the user select one using the SmartDashboard.
        
        # SmartDashboard interface
        self.sd = wpilib.SmartDashboard
        
        #
        #    Control mode chooser
        #
        #    This chooser chooses the mode that we will decide what we do during
        #    during the Operator Control Phase, we use a BiDirectionChooser
        
        self.control_mode_chooser = wpilib.SendableChooser()
        
        print("Loaded operator control modes:")
        for k,v in self.modes.items():
            
            if hasattr(v, 'DEFAULT') and v.DEFAULT == True:
                print(" -> %s [Default]" % k)
                self.control_mode_chooser.AddDefault(k, v)
            else:
                print( " -> %s" % k )
                self.control_mode_chooser.AddObject(k, v)
                
        # must PutData after setting up objects
        self.sd.PutData('Operator Control Mode', self.control_mode_chooser)
        
        print( "OperatorControlManager::__init__() Done" )
    
            
    def run(self, robot, control_loop_wait_time):    
        '''
            This function does everything required to implement operator control
            mode behavior. 
            
            :param robot: a SimpleRobot derived class, and is expected to 
                          have a function called 'update', which will do 
                          updates on all motors and components.
                          
        '''
        
        print("OperatorControlManager::operator ()")
             
        try:
            self.on_operator_control_enable()
        except:
            if not self.ds.IsFMSAttached():
                raise
        
        # get the watchdog
        dog = robot.GetWatchdog()

        #
        # operator control loop
        #
        
        delay = PreciseDelay(control_loop_wait_time)
        
        #
        # Initialize into load mode on operator control switch
        #
        self.set_selected("Load Mode")
        
        while robot.IsOperatorControl () and robot.IsEnabled():
            # measure loop time
            start = wpilib.Timer.GetPPCTimestamp()
            try:
                #all driving is done the same so we will do it here to not cluter our
                #different modes, also controller mode changes shall be handled here
                
                #
                #Drive
                #
                y_axis = stick_axis(L_AXIS_Y,self.ds)
                twist =  stick_axis(R_AXIS_X,self.ds)
                x_axis = stick_axis(L_AXIS_X,self.ds)
                
                #self.led_strip.set_led_color(1, 255, 0, 0, repeat = self.led_strip.get_num_leds())
                

                self.robot_drive.MecanumDrive_Cartesian(x_axis, y_axis, twist )
                
                
                #
                #these are exclusionary, change the mode based on user input
                #if no user input check if there is a next mode and set to it
                #if there is
                #
                if stick_button_on(1,self.ds):
                    print("robot: loading mode")
                    self.set_selected("Loading Mode")
                    
                    
                elif stick_button_on(2,self.ds): 
                    print("robot: passing mode")
                    self.set_selected("Passing Mode")
                    
                elif stick_button_on(3,self.ds): 
                    print("robot: shooting mode")
                    self.set_selected("Shooting Mode")
                
                #
                # all components have an auto and a manual mode these are 
                # selected here, if in an auto mode then the choosen mode
                # will handle the control, if not they will be handled by 
                # this object in set        
                #
                #switch between if we can auto load or not
                if stick_axis(D_PAD_AXIS_X,self.ds) > 0:
                    self.sd.PutBoolean('auto load', True)
                if stick_axis(D_PAD_AXIS_X,self.ds) < 0:
                    self.sd.PutBoolean('auto load', False)
                
                #
                #switch between if the scam is auto
                #
                if stick_button_on(SELECT,self.ds):
                    self.sd.PutBoolean('auto scam', False)
                
                if stick_button_on(START,self.ds):
                    self.sd.PutBoolean('auto scam', True)
                
                #
                #Manual igus_slide
                #
                
                if stick_axis(D_PAD_AXIS_Y,self.ds) < 0:
                    self.sd.PutBoolean('auto igus', False)
                    
                elif stick_axis(D_PAD_AXIS_Y,self.ds) > 0:
                    self.sd.PutBoolean('auto igus', True)
                
                self.set()
            except:
                if not self.ds.IsFMSAttached():
                    raise
            
            robot.update()
            dog.Feed()
            
            delay.wait()
            
            
            # how long does it take us to run the loop?
            # -> we're using a lot of globals, what happens when we change it?
            wpilib.SmartDashboard.PutNumber('Loop time', wpilib.Timer.GetPPCTimestamp() - start)
            
            
        try:
            self.on_operator_control_disable()
        except:
            if not self.ds.IsFMSAttached():
                raise
    
    #
    #   Internal methods used to implement operator  mode switching. Most
    #   users of this class will not want to use these functions, use the
    #   run() function instead. 
    #
    
    def on_operator_control_enable(self):
        '''Select the active operator control mode here, and enable it'''
        self.active_mode = self.control_mode_chooser.GetSelected()
        if self.active_mode is not None:
            print("OperatorControlManager: Enabling %s" % self.active_mode.MODE_NAME)
            self.active_mode.on_enable()
 
    def on_operator_control_disable(self):
        '''Disable the active operator control'''
        if self.active_mode is not None:
            print("OperatorControlManager: Disabling %s" % self.active_mode.MODE_NAME)
            self.active_mode.on_disable()
            
        self.active_mode = None
        
    def set(self): 
        '''Select the active operator control mode here, and enable it'''
      
        auto_load = self.sd.GetBoolean('auto load')
        auto_scam = self.sd.GetBoolean('auto scam')
        auto_igus = self.sd.GetBoolean('auto igus')
        
        # switch mode if neccessary  
        previous_mode = self.active_mode
        self.active_mode = self.control_mode_chooser.GetSelected()
        
        if self.active_mode is not None:
            if self.active_mode is not previous_mode:
                print("OperatorControlManager: Enabling %s" % self.active_mode.MODE_NAME)
                self.active_mode.on_enable()
                
            '''
                Run the code for the current operator control mode, if return not none then set the 
                mode of the robot based on the return
            '''
            next_mode = self.active_mode.set(auto_load, auto_scam, auto_igus)
            
            if not auto_scam:
                self.modes["Manual Mode"].manual_scam()
                
            if not auto_igus:
                self.modes["Manual Mode"].manual_igus()
                
            if next_mode != None: 
                if next_mode not in self.modes:
                    print("ERROR: Mode return not in modes")
                else:
                    print("Auto mode change: ", next_mode)
                    self.set_selected(next_mode)
            
    def set_selected(self, selected):
        self.control_mode_chooser.GetTable().PutString('selected', selected)
        
