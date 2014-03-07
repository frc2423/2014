'''
    Author:  Sam Rosenblum
    Date:    2/11/2013
    Updated: 2/25/2013
    
    This file holds the class GenericDistanceSensor which holds with in it
    equations that holds a map that represent best fit equations for different 
    types of distance sensors
'''

import math
from common.constants import *

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

# sensors
GP2D120 = 0
MB10X3  = 1 #covers MB1003, MB1013, MB1023

# settings
METRIC = 0
ENGLISH = 1


class GenericDistanceSensor(wpilib.AnalogChannel):

    # For each sensor type, define a function that translates the voltage 
    # to a distance (in cm units)
    SENSOR_EQUATIONS = {
        GP2D120: lambda v: math.pow((v/11.036), -1/.947),
        MB10X3:  lambda v: v * (512/5), #document states distance per mm is 5120/vcc with a 5mm accuracy
                                        #this function outputs cm  
    }
    
    def __init__(self, channel, sensor_type, system=ENGLISH): 
        '''
            constructor takes a channel and a sensor_type to figure out the
            real distance
            
            :param channel: The channel number for the associated analog sensor
        '''
        
        super().__init__(channel)
        
        self.distance_fn = self.SENSOR_EQUATIONS[sensor_type]
        self.system = system
    
        
    def GetDistance(self):
        '''gets distance in cm based on the voltage''' 
        v = self.GetVoltage()
        
        # if the value is zero, return zero
        if v <= 0:
            return 0
    
        # convert the voltage to a distance
        distance = self.distance_fn(v)
        
        # convert to appropriate units
        if self.system == ENGLISH:
            distance /= INCH_TO_CM
        return distance
      
        
    def GetAverageDistance(self):
        '''Gets average distance based on average voltage'''
        
        v = self.GetAverageVoltage()
                
        # if the value is zero, return zero
        if v <= 0:
            return 0
    
        # convert the voltage to a distance
        distance = self.distance_fn(v)
        
        # convert to appropriate units
        if self.system == ENGLISH:
            distance /= INCH_TO_CM
        
        return distance
