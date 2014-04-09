'''
    logitech joystick util functions and constants, there is no need to create the overhead
    of an object here. Only one controller is used this year so it is fine to not use any
    tuples 
'''
try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

from common.logitech_controller import *
#
#    Joystick utility functions (yay overhead!)
#

def stick_axis(axis, ds):
    return ds.GetStickAxis(1, axis)

def translate_axis(axis, amin, amax, ds):
    '''Returns an axis value between a min and a max'''
    a = ds.GetStickAxis(1, axis)
    
    # Xmax - (Ymax - Y)( (Xmax - Xmin) / (Ymax - Ymin) )
    return amax - ((1 - a)*( (amax - amin) / 2.0 ) )
    
def stick_button_on(button , ds):
    return ds.GetStickButtons( 1 ) & (1 << (button -1))