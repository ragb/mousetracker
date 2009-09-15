#! /usr/bin/env python

import pygtk
pygtk.require("2.0")

import gobject
import gtk
import pyatspi

from trackers import MousePositionTracker

import settings

class Application(object):

    def __init__(self):
        pass

    def main(self, argv):
        self._settings = settings.Settings()
        # setup signal handlers
        import signal
        signal.signal(signal.SIGINT, lambda signum, stackframe : self.quit())

        # startup sound tracker
        kwargs = {}
        if 'positiontracker' in self._settings:
            kwargs = self._settings['positiontracker']
        self._tracker = MousePositionTracker(**kwargs)
        self._tracker.run()
        pyatspi.Registry.start()

    def quit(self):
        self._tracker.stop()
        pyatspi.Registry.stop()
        
        self._settings['positionTracker'] = self._tracker.getPropertiesAsDict()
        self._settings.flush()

if __name__ == '__main__':
    import sys
    Application().main(sys.argv)
