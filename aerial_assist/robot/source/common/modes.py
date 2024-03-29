'''
    Contains all the different types of modes shared between the robot components
'''
SHOOT_MODE = 0
LOAD_MODE = 1
PASS_MODE = 2

#auto or manual of component
MANUAL = 0
AUTO = 1

mode_dict = {
                SHOOT_MODE: "SHOOT_MODE",
                LOAD_MODE:  "LOAD_MODE",
                PASS_MODE:  "PASS_MODE",
                None:       "None"
             }

auto_mode_dict = {
                    MANUAL: "MANUAL",
                    AUTO: "AUTO"
                  }