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
        settings.init()
        # setup signal handlers
        import signal
        signal.signal(signal.SIGINT, lambda signum, stackframe : self.quit())

        # load configuration
        # startup sound tracker
        kwargs = settings.getSection("positiontracker")
        self._tracker = MousePositionTracker(**kwargs)
        self._tracker.run()
        pyatspi.Registry.start()

    def quit(self):
        self._tracker.stop()
        pyatspi.Registry.stop()
        settings.flush()

if __name__ == '__main__':
    import sys
    Application().main(sys.argv)
