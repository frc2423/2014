#    robot - This is whatever is returned from the run function in robot.py
#    wpilib - This is the wpilib module
import time

def test_operator_control(robot, wpilib):

    
    class TestController(object):
        '''This object is only used for this test'''
    
        loop_count = 0
        
        
        #Modes
        
        
        def IsOperatorControl(self, tm):
            '''
                Continue operator control for 1000 control loops
            '''
            
            self.loop_count += 1
            return not self.loop_count == 1000

    
    wpilib.internal.set_test_controller(TestController)
    wpilib.internal.enabled = True
    robot.OperatorControl()
    
    # do something like assert the motor == stick value

