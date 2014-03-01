#
#   This file is part of KwarqsDashboard.
#
#   KwarqsDashboard is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, version 3.
#
#   KwarqsDashboard is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with KwarqsDashboard.  If not, see <http://www.gnu.org/licenses/>.
#


import math
import os

import gtk

import ui.util

class RobotWidget(gtk.DrawingArea):
    '''
        When the robot reports the angle of the platform, draw the
        platform on the UI at that particular angle. 
        
        Additionally, show frisbees on the platform, and move them with
        it. In practice, operators rarely use this widget. However, its 
        a great visual aid for demonstrations, or for debugging the 
        robot. 
    
        TODO: Make this more general, we hardcoded everything here
    '''
    
    def __init__(self, table):
        gtk.DrawingArea.__init__(self)
        
        self.table = table
        self.angle = 0
        self.robot = ui.util.pixbuf_from_file('Robot-bace.gif')
        
        # size request
        self.set_size_request(self.robot.get_width(), self.robot.get_height())
        
        self.connect('expose-event', self.on_expose)
        
        
    def set_angle(self, angle):
        if angle < -30:
            angle = -30.0
        elif angle > 65.0:
            angle = 65.0
        
        if angle != self.angle:
            self.angle = angle
            self.queue_draw()
        
    def get_ball_roller_angle(self, angle):
        if angle > 30:
            return 0
        else:
            return (-angle + 30)
        
    def on_expose(self, widget, event):
        
        # background
        event.window.draw_pixbuf(None, self.robot, 0, 0, 0, 0)
        
        cxt = event.window.cairo_create()
        
        # angle text
        cxt.move_to(30, 30)
        cxt.set_font_size(20)
        cxt.show_text('%.2f' % self.angle)
        
        cxt.set_source_rgb(0,0,0)
        cxt.fill_preserve()
        cxt.stroke()
        
        cxt.set_line_width(3)
        cxt.set_source_rgb(0,0,0)
        #draw bar for scam
        cxt.move_to(120, 205)
        cxt.line_to(120, 140)
        
        #set rotation point 
        cxt.translate(120,140)
        cxt.rotate(math.radians(-self.angle))
        cxt.translate(-120,-140)
        
        #igus
        cxt.set_line_width(3)
        cxt.set_source_rgb(0,0,0)
        cxt.move_to(50, 140)
        cxt.line_to(290, 140)
        cxt.stroke()
        #shuttle
        cxt.move_to(60, 140)
        cxt.line_to(60, 115)
        cxt.stroke()
        
        #reorient
        cxt.translate(120,140)
        cxt.rotate(math.radians(self.angle))
        cxt.translate(-120,-140)
        
        cxt.translate(240,205)
        cxt.rotate(math.radians(self.get_ball_roller_angle(self.angle)))
        cxt.translate(-240,-205)
        
        #ball roller bar
        cxt.move_to(240,205)
        cxt.line_to(240, 120)
        cxt.stroke()

        

