'''
    This code is based on C++ code by adafruit for the WS2801 chip. It is designed
    to simply set the color of individual leds or of a strip of leds via wpilibs 
    spi bus
'''

import threading

try:
    import wpilib
except ImportError:
    from pyfrc import wpilib

#possible arrangements of leds
NO_ARRANGEMENT = 0
AM_2640       = 1

#rgd order
RGB = 0
BGR = 1

# to avoid magic numbers R,G,B are used in indexs of our data array
R = 0
G = 1
B= 2

#set clock rate to 60hz?
CLOCK_RATE = 60000

#dictionary of conversions from input to real number of leds, it is in per inch configuration
ARRANGMENT_NUM_LEDS = {
    NO_ARRANGEMENT: lambda n:n,
    AM_2640: lambda n:int(n/1.23), #there is 1.23 inches to each led
}

class ws2801_led(object):
    
    def __init__(self, leds, SPI, arrangment = AM_2640, order = RGB):
        '''
            initializes the led object
            
            parameters:
                leds - defines the number of leds, if arrangement is NO_ARRANGMENT
                       then this means that that leds means number of leds, if 
                       it is AM_2640 then it means inches of length of the strip
                       
                SPI - an spi object
                
                arrangement - the type of arrangment of the leds, defines what leds actually means
           
                order - order data should go to leds RGB or BGR 
        
            variables:
                SPI - our spi bus
                num_leds - number of leds in this instance
                order - order of data rgb or bgr
                led_data - representation of led pixels
        '''
        
        self.SPI = SPI
        
        #tells us how many leds we have
        self.num_leds = ARRANGMENT_NUM_LEDS[arrangment](leds)
        
        self.order = order
        
        #init our data array
        self.led_data = [[0,0,0] for leds in range(self.num_leds)] 
        
        self.config_spi()
        
        self.lock = threading.Lock()
        
    def config_spi(self):
        '''
            configures spi to correct configuration for the ws2801
        '''
        self.SPI.SetMSBFirst()
        self.SPI.SetClockActiveLow()
        self.SPI.SetSampleDataOnFalling()
        self.SPI.SetClockRate(CLOCK_RATE)
        
        #set word rate
        self.SPI.SetBitsPerWord(8)
        
        #apply the config
        self.SPI.ApplyConfig()
        
    def get_num_leds(self):
        return self.num_leds
 
    def set_led_color(self, pixel, r, g, b, repeat = 0):
        '''
            sets color of a specific led, should not set or change while
            we are changing colors
            
            pixel - pixel to set
            r - red component
            g - green component
            b - blue component
            repeat = how many pixels after pixel to change to the same color
            
        '''
        if(self.lock.acquire(False)):
            if pixel >= self.num_pixels:
                return False
            
            self.led_data[pixel] = r, g ,b
                
            #write for repeat times if repeat times is ends up going past num_led
            #write only till num led
            if (pixel + repeat) >= self.num_leds:
                repeat = self.num_leds - pixel
                
            for led in self.led_data[pixel:pixel - repeat]:
                led = r, g, b
        
    def threaded_update(self):
        '''
            to be called as a thread so as not to prevent regular operation when
            doing light stuff
        '''
        for led in self.led_data:
            if self.order == RGB:
                for color in led:
                    self.SPI.Write(color)
                    self.wait(.001)# Data is latched by holding clock pin low for 1 millisecond
        
        self.lock.release()
        
    def update(self):
        '''
            updates the colors on the actual leds
        '''
        if(self.lock.acquire(False)):
            t = threading.Thread(target=self.threaded_update)
            t.start()
            
        
        
        
        
        
        
        
        