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
            
            
            if self.loop_count >= 1:
                LOAD = robot.LOAD_MODE
                PASS = robot.PASS_MODE
                SHOOT = robot.SHOOT_MODE
                components = [robot.BallRoller, robot.IgusSlide, robot.Scam]
        
            if self.loop_count <= 200 and self.loop_count >= 1:
                robot.button_two = True
                time.sleep(.1)
                for component in components:
                    assert component.mode == LOAD or component.mode == SHOOT
                robot.button_two = False
                
            elif self.loop_count >= 201 and self.loop_count <= 400:
                robot.l_trigger = True
                time.sleep(.1)
    
                for component in components:
                    assert component.mode == PASS
                robot.l_trigger = False
                
            
            self.loop_count += 1
            return not self.loop_count == 1000

    
    wpilib.internal.set_test_controller(TestController)
    wpilib.internal.enabled = True
    robot.OperatorControl()
    
    # do something like assert the motor == stick value

