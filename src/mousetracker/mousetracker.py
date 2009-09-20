#! /usr/bin/env python

import sys

import gobject
import pyatspi

import dbus
import dbus.service
import dbus.mainloop
import dbus.glib

import logging

from trackers import MousePositionTracker

import settings

BUS_NAME = "mousetracker.Daemon"
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

_log = logging.getLogger("mousetracker")
_handler = logging.StreamHandler()
_log.addHandler(_handler)
_log.setLevel(logging.DEBUG)

class Daemon(object):

    def __init__(self, args=[]):
    
    # read configuration
                self._settings = settings.Settings()
                
                # store reference to session bus
                self._bus = dbus.SessionBus()
                self._bus_name = None

    def main(self):
        # setup signal handlers
        import signal
        signal.signal(signal.SIGINT, lambda signum, stackframe : self.quit())

        # verfify if there is another instance of the daemon running
        if self._busNameInUse():
            _log.critical("Bus name already in use, another daemon instance is running on your system. Exiting now.")
            sys.exit(-1)
        # store reference to bus_name
        self._bus_name = dbus.service.BusName(BUS_NAME, bus=dbus.SessionBus())

        # startup sound tracker
        kwargs = {}
        if 'positiontracker' in self._settings:
            kwargs = self._settings['positiontracker']
        self._tracker = MousePositionTracker(**kwargs)
        self._tracker.running = True
        
        _log.info("Starting Daemon")
        pyatspi.Registry.start()

    def quit(self):
        self._tracker.running = False
        self._settings['positionTracker'] = self._tracker.getAll()
        self._settings.flush()
        pyatspi.Registry.stop()
        _log.info("Daemon stoped")

    def _busNameInUse(self):
        daemon_proxy = self._bus.get_object(dbus.BUS_DAEMON_NAME, dbus.BUS_DAEMON_PATH)
        return daemon_proxy.NameHasOwner(BUS_NAME, dbus_interface=dbus.BUS_DAEMON_IFACE)

if __name__ == '__main__':
    Daemon(sys.argv).main()
