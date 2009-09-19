#! /usr/bin/env python

import pygtk
pygtk.require("2.0")

import gobject
import gtk
import pyatspi

import dbus
import dbus.service
import dbus.mainloop
import dbus.glib

from trackers import MousePositionTracker

import settings

BUS_NAME = "mousetracker.daemon"
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

class Daemon(object):

    def __init__(self):
        pass

    def main(self, argv):
        self._settings = settings.Settings()
        # setup signal handlers
        import signal
        signal.signal(signal.SIGINT, lambda signum, stackframe : self.quit())

        # store reference to bus
        self._bus = dbus.service.BusName(BUS_NAME, bus=dbus.SessionBus())

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
        
        self._settings['positionTracker'] = self._tracker.getAll()
        self._settings.flush()

if __name__ == '__main__':
    import sys
    Daemon().main(sys.argv)
