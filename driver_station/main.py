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

    from common import logutil, settings
    from options import configure_options

    # ok, import stuff so we can get their versions
    import pygtk
    pygtk.require('2.0')
    import gtk

    import gobject
    import glib

    import cairo

    import cv2
    import numpy as np

    # do this first, just in case
    gobject.threads_init()

    def initialize_pynetworktables(ip):
        
        if ip is not None:
            
            from pynetworktables import NetworkTable
            
            NetworkTable.SetIPAddress(ip)
            NetworkTable.SetClientMode()
            NetworkTable.Initialize()
            
            return NetworkTable.GetTable('SmartDashboard')
        

    if __name__ == '__main__':
        
        # get options first
        parser = configure_options()
        options, args = parser.parse_args()
        
        #tells us if we are to load camera based widget or not
        no_cam = options.no_cam
        
        # initialize logging before importing anything that uses logging!
        ql = logutil.configure_logging(options.log_dir)
        
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info('Starting Kwarqs Dashboard')

        # show versions
        logger.info('-> Python %s' % sys.version.replace('\n', ' '))
        logger.info('-> GTK %s.%s.%s' % gtk.gtk_version)
        logger.info('-> Cairo %s' % cairo.version)
        logger.info('-> NumPy %s' % np.__version__)
        logger.info('-> OpenCV %s' % cv2.__version__)
        
        # configure and initialize things    
        table = initialize_pynetworktables(options.robot_ip)

        processor = None
        
        # initialize UI
        import ui.dashboard
        dashboard = ui.dashboard.Dashboard(processor, table, options.competition, no_cam)
        
        # initialize cv2.imshow replacement
        import ui.widgets.imshow
        
        # gtk main
        dashboard.show_all()
        
        #gtk.threads_init()
            
        #gtk.threads_enter()
        gtk.main()
        #gtk.threads_leave()
        
        
        logger.info('Shutting down Kwarqs Dashboard')
        settings.save()
        
        if not no_cam:
            # shutdown anything needed here, like the logger
            processor.stop()
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
