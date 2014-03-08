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

import gtk

import util
from widgets import camera_widget, preprocessor_tuning_widget, robot_widget, image_button, toggle_button 

import logging
logger = logging.getLogger(__name__)


class Dashboard(object):
    '''
        This holds the main UI for the Kwarqs dashboard program. Ideally, we
        should ship most of the logic out of this class and do things
        elsewhere. Of course.. that's not quite the case now. 
    '''
    
    ui_filename = 'dashboard.ui'
    ui_widgets = [
        'window',
        
        'camera_widget',
        'robot_widget',
        
        'control_notebook',
               
        'passing_mode_button',
        'loading_mode_button',
        'manual_mode_button',
        'shooting_mode_button',
        
        'shoot_angle_button',
        'max_angle_button',
        'truss_angle_button',
        
        'shuttle_status',
        'ready_status',
        'angle_status',
        
        'fire_button',
        
        'auto_scam_button',
        'auto_load_button',
        'auto_retract_button',
        
        'targeting_tuning_widget'
    ]
    ui_signals = [
        'on_window_destroy',
    ]
    
    # keep in sync with robot
    MODE_DISABLED       = 1
    MODE_AUTONOMOUS     = 2
    MODE_TELEOPERATED   = 3
    
    def __init__(self, processor, table, competition, no_cam = False):
        
        self.processor = processor
        self.no_cam = no_cam
        if no_cam == False:
            
            camera = camera_widget.CameraWidget((640,480))
            self.processor.set_camera_widget(camera)
        else:    
            self.ui_filename = 'dashboard_no_cam.ui'
        
        util.initialize_from_xml(self)
        
        if no_cam != True:
            self.camera_widget = util.replace_widget(self.camera_widget, camera)
        #util.replace_widget(self.targeting_tuning_widget, self.targeting_tuner.get_widget())

        self.robot_widget = util.replace_widget(self.robot_widget, robot_widget.RobotWidget(table))

        #self.targeting_tuner.initialize()
       
        self.table = table
        
        self.window.set_title("Kwarqs Dashboard")
        self.window.connect('realize', self.on_realize)
       
        if competition:
            self.window.move(0,0)
            self.window.resize(1356, 525)
            
        # load the status buttons
        active_pixbuf = util.pixbuf_from_stock(gtk.STOCK_YES, gtk.ICON_SIZE_BUTTON)
        inactive_pixbuf = util.pixbuf_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)
        
        for name in ['shuttle_status','ready_status','angle_status']:
            old_widget = getattr(self, name)
            text = old_widget.get_label()
            setattr(self, name, util.replace_widget(old_widget, toggle_button.ToggleButton(active_pixbuf, inactive_pixbuf, text, clickable=False, default=False)))
            
        #load the angle buttons
        for mode in ['truss', 'shoot', 'max']:
            active = util.pixbuf_from_file('angle_' + mode + '_active.png')
            inactive = util.pixbuf_from_file('angle_' + mode + '_inactive.png')
            name = '%s_angle_button' % mode
            setattr(self, name, util.replace_widget(getattr(self, name), toggle_button.ToggleButton(active, inactive, clickable=True, default=False)))
            
        # setup the mode buttons
        for mode in ['passing', 'loading', 'manual', 'shooting']:
            active = util.pixbuf_from_file(mode + '-on.png')
            inactive = util.pixbuf_from_file(mode + '-off.png')
            name =  '%s_mode_button' % mode
            setattr(self, name, util.replace_widget(getattr(self, name), toggle_button.ToggleButton(active, inactive, clickable=True, default=False)))
            
        # setup the fire button
        active = util.pixbuf_from_file('fire-on.png')
        inactive = util.pixbuf_from_file('fire-off.png')
        self.fire_button = util.replace_widget(self.fire_button, image_button.ImageButton(inactive))
        self.fire_button.connect('clicked', self.on_fire_clicked)
        
        # save these for later
        self.fire_button.active_pixbuf = active
        self.fire_button.inactive_pixbuf = inactive
        
        # setup the toggle buttons
        active = util.pixbuf_from_file('toggle-on.png')
        inactive = util.pixbuf_from_file('toggle-off.png')
        
        for name in [ 'auto_scam_button','auto_load_button','auto_retract_button',]:
            setattr(self, name, util.replace_widget(getattr(self, name), toggle_button.ToggleButton(active, inactive, clickable=True, default=False)))
        
        
            
        # connect widgets to pynetworktables
        if self.table is not None:
            
            # don't import this unless we have a table, so we can support running
            # on a laptop without networktables
            import ui.widgets.network_tables as nt
            
            nt.attach_toggle(table, 'auto load', self.auto_load_button)
            nt.attach_toggle(table, 'auto scam', self.auto_scam_button)
            nt.attach_toggle(table, 'auto igus', self.auto_retract_button)
            
            #angle chooser
            angle_select_widgets = {'shoot angle': self.shoot_angle_button,
                                    'truss angle': self.truss_angle_button,
                                    'max angle': self.max_angle_button}
            
            nt.attach_chooser_buttons(table, 'Shooting Goal', angle_select_widgets)
            
            # other chooser
            widgets = {'Passing Mode': self.passing_mode_button, 
                       'Loading Mode': self.loading_mode_button,
                       'Manual Mode': self.manual_mode_button,
                       'Shooting Mode': self.shooting_mode_button }
            
            nt.attach_chooser_buttons(table, 'Operator Control Mode', widgets)
            
            # robot widget
            nt.attach_fn(table, 'Scam Angle', lambda k, v: self.robot_widget.set_angle(v), self.robot_widget)
            
            
            # modes
            nt.attach_fn(table, 'Robot Mode', self.on_robot_mode_update, self.window)
            
            # connection listener
            nt.attach_connection_listener(table, self.on_connection_connect, self.on_connection_disconnect, self.window)
       
    def on_connection_connect(self, remote):
        
        # this doesn't seem to actually tell the difference
        if remote.IsServer():
            logger.info("NetworkTables connection to robot detected")
        else:
            logger.info("NetworkTables connection to client detected")
            
        if self.no_cam != True:   
            self.processor.start()
            self.camera_widget.start()
        
    def on_connection_disconnect(self, remote):
        if remote.IsServer():
            logger.info("NetworkTables disconnected from robot")
        else:
            logger.info("NetworkTables disconnected from client")
       
    def on_robot_mode_update(self, key, value):
        value = int(value)
        if value == self.MODE_AUTONOMOUS:
            if self.processor != None:
                self.processor.enable_image_logging()
            
            logger.info("Robot switched into autonomous mode")
            logger.info("-> Current mode is: %s", current_mode)
            self.control_notebook.set_current_page(0)
            
            
        elif value == self.MODE_TELEOPERATED:
            if self.processor != None:
                self.processor.enable_image_logging()
            
            logger.info("Robot switched into teleoperated mode")
            self.control_notebook.set_current_page(1)
            
            
        else:
            # don't waste disk space while the robot isn't enabled
            
            self.processor.disable_image_logging()
            
            logger.info("Robot switched into disabled mode")
            self.control_notebook.set_current_page(0)
              
        
    def update_ready_status(self):
        active = self.shuttle_status.get_active() and self.angle_status.get_active()
                 
        self.ready_status.set_active(active)   
        if active:
            self.fire_button.set_from_pixbuf(self.fire_button.active_pixbuf)
        else:
            self.fire_button.set_from_pixbuf(self.fire_button.inactive_pixbuf)  
        
    def show_all(self):
        self.window.show_all()
        
    def on_realize(self, widget):
        sz = self.window.get_allocation()
        logger.info('Dashboard window size is %sx%s', sz.width, sz.height)
        
    
    def on_window_destroy(self, widget):
        gtk.main_quit()
        
        
    def on_fire_clicked(self, widget):
        
        # presumably when the user fires, they want to remain stationary
        # -> TODO: but, in case they change their mind, we should restore it
        #    in autotargeting mode. But what does that really mean? This
        #    is in case they miss and need to adjust. Maybe what we really
        #    want is to disable autotargeting when the wheel is on... but 
        #    that's probably not the case either. Think this use case through!
        
        if self.table is not None:
            self.table.PutBoolean("Fire", True)
        