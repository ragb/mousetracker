#! /usr/bin/env python

import pygtk
pygtk.require("2.0")

import gobject
import gtk
import pyatspi

from trackers import MousePositionTracker


class Application(object):

    def __init__(self):
        pass

    def main(self, argv):

    # setup signal handlers
        import signal
        signal.signal(signal.SIGINT, lambda signum, stackframe : self.quit())

        # startup sound tracker
        self._tracker = MousePositionTracker()
        self._tracker.run()
        pyatspi.Registry.start()

    def quit(self):
        self._tracker.stop()
        pyatspi.Registry.stop()

if __name__ == '__main__':
    import sys
    Application().main(sys.argv)
