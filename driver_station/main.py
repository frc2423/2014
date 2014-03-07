'''
    This file is part of KwarqsDashboard.

    KwarqsDashboard is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    KwarqsDashboard is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with KwarqsDashboard.  If not, see <http://www.gnu.org/licenses/>.
'''


import sys

try:

    import sys
    
    if sys.version_info[0] != 2:
        sys.stderr.write("ERROR: Unsupported python version %s.%s.%s! This program must be run by a Python 2 interpreter!\n" % \
                          (sys.version_info[0],
                           sys.version_info[1],
                           sys.version_info[2]))
        exit(1)

    from common import logutil, image_capture, settings
    from options import configure_options


    import cv2
    import numpy as np


    def initialize_pynetworktables(ip):
        
        if ip is not None:
            
            from pynetworktables import NetworkTable
            
            NetworkTable.SetIPAddress(ip)
            NetworkTable.SetClientMode()
            NetworkTable.Initialize()
            
            return NetworkTable.GetTable('SmartDashboard')
        

    if __name__ == '__main__':
        
        camera_processor = image_capture.ImageCapture()
        
        # get options first
        parser = configure_options()
        camera_processor.configure_options(parser)
        
        options, args = parser.parse_args()
        
        #tells us if we are to load camera based widget or not
        no_cam = options.no_cam
        
        # initialize logging before importing anything that uses logging!
        ql = logutil.configure_logging(options.log_dir)
        
        import logging
        logger = logging.getLogger(__name__)
        

        # automatically load pygtk in windows, since the setup is annoying
        if sys.platform == 'win32':
            from common import load_pygtk_windows
            load_pygtk_windows.load_pygtk()
        else:
            import pygtk
            pygtk.require('2.0')
            
        # ok, import stuff so we can get their versions
        import gtk
    
        import gobject
        import glib
    
        import cairo
        
        # do this first, just in case
        gobject.threads_init()
        
        logger.info('Starting Kwarqs Dashboard')
        
        # show versions
        logger.info('-> Python %s' % sys.version.replace('\n', ' '))
        logger.info('-> GTK %s.%s.%s' % gtk.gtk_version)
        logger.info('-> Cairo %s' % cairo.version)
        logger.info('-> NumPy %s' % np.__version__)
        logger.info('-> OpenCV %s' % cv2.__version__)
        
        # configure and initialize things    
        table = initialize_pynetworktables(options.robot_ip)
        
        if no_cam:
            camera_processor = None
        
        # initialize UI
        import ui.dashboard
        dashboard = ui.dashboard.Dashboard(camera_processor, table, options.competition, no_cam)
        
        # initialize cv2.imshow replacement
        import ui.widgets.imshow
        
        if not no_cam:
            try:
                camera_processor.initialize(options)
            except RuntimeError:
                exit(1)
            
        # gtk main
        dashboard.show_all()
        
                #
        # FFMpeg/OpenCV doesn't handle connecting to non-existent cameras
        # particularly well (it hangs), so when we're using a live feed, delay 
        # connecting to the camera (ie, starting processing) until the 
        # NetworkTables client has connected to a robot.
        #
        # Presumably if we can talk to the robot, we can talk to the camera 
        # also. If we're not using a live feed, then just start it regardless.  
        # 
        if not no_cam:
            if table is None or not camera_processor.is_live_feed():
                camera_processor.start()
            
        #gtk.threads_init()
            
        #gtk.threads_enter()
        gtk.main()
        #gtk.threads_leave()
        
        
        logger.info('Shutting down Kwarqs Dashboard')
        settings.save()
        
        if not no_cam:
            # shutdown anything needed here, like the logger
            camera_processor.stop()
            
        ql.stop()


except Exception as e:

    if __name__ == '__main__':
        import traceback
        traceback.print_exc()
    
        try:
            import msvcrt
        except ImportError:
            pass
        else:        
            msvcrt.getch()
    else:
        raise
