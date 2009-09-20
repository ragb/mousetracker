"""
Mouse trackers

For now it has just the BeepsMouseTracker
"""

import pygtk
pygtk.require("2.0")
import gtk

import pygst
pygst.require("0.10")
import gst

import gobject
import pyatspi

import dbus
import dbus.service
import dbus.gobject_service

import logging

class TrackerPropertyException(dbus.DBusException):
    _dbus_error_name="mousetracker.tracker.TrackerPropertyException"

class MouseTracker(dbus.gobject_service.ExportedGObject):
    _log = logging.getLogger("mousetracker.tracker")
    _log.setLevel(logging.DEBUG)

    PROPERTIES_IFACE = "mousetracker.tracker.Properties"

    def __init__(self, **kwargs):
        from mousetracker import BUS_NAME
        dbus.gobject_service.ExportedGObject.__init__(self, conn=dbus.SessionBus(),
            bus_name=dbus.service.BusName(BUS_NAME, bus=dbus.SessionBus()), **kwargs)
        self.connect("notify", self._onPropertyChanged)

    @dbus.service.method(PROPERTIES_IFACE,
    in_signature="",
    out_signature="a{sv}")
    def getAll(self):
        dict = {}
        for prop in self.props:
            dict[prop.name] = self.get_property(prop.name)
        self._log.debug("getAll method called. Properties are %s" % str(dict))
        return dict

    @dbus.service.method(PROPERTIES_IFACE,
in_signature="s",
out_signature="v")
    def get(self, name):
        try:
            self._log.debug("Get %s=%s." %(name, value))
            return self.get_property(name)
        except TypeError, e:
            self._log.exception(e)
            raise TrackerPropertyError(e.message)

    @dbus.service.method(PROPERTIES_IFACE,
    in_signature="sv",
    out_signature="")
    def set(self, property, value):
        try:
            self._log.debug("Set %s=%s." %(name, value))
            self.set_property(property, value)
        except TypeError, e:
            self._log.exception(e)
            raise TrackerPropertyError(e.message)

    def _onPropertyChanged(self, object, spec, userdata=None):
        name = spec.name
        value = self.get_property(name)
        self.propertyChanged(name, value)

    @dbus.service.signal(PROPERTIES_IFACE,
    signature="sv")
    def propertyChanged(self, name, value):
        self._log.debug("Notifying of %s changing to %s" % (name, value))
        return (name, value)

class MousePositionTracker(MouseTracker):
    """ Mouse locator class to locate the mouse using sound """
    object_path = "/mousetracker/tracker/MousePositionTracker"

    def __init__(self, **kwargs):
        self._running = False
        MouseTracker.__init__(self, object_path=MousePositionTracker.object_path, **kwargs)
        # construct pipeline
        self._player = gst.Pipeline()
        self._source = gst.element_factory_make("audiotestsrc")
        self._source.set_property("num_buffers", 5)
        self._source.set_property("wave", 3)
        self._panorama = gst.element_factory_make("audiopanorama")
        self._converter = gst.element_factory_make("audioconvert")
        self._sink = gst.element_factory_make("gconfaudiosink")
        self._player.add(self._source, self._panorama, self._converter, self._sink)
        gst.element_link_many(self._source, self._panorama, self._converter, self._sink)
        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._onMessage)

    def _get_volume(self):
        return self._source.get_property("volume")

    def _set_volume(self, volume):
        self._source.set_property("volume", volume)

    volume = gobject.property(
        type=float,
        nick='volume',
        default=0.5,
        minimum=0.0,
        maximum=1.0,
        getter=_get_volume,
        setter=_set_volume
        )

    max_freq = gobject.property(
        type=int,
        nick='max_freq',
        default=1500,
        minimum=600,
        maximum=2000
        )

    min_freq = gobject.property(
        type=int,
        nick='min_freq',
        default=200,
        minimum=20,
        maximum=500
        )

    def _get_running(self):
        try:
            return self._running
        except AttributeError:
            return False

    def _set_running(self, value):
        if value != self._running: # if it is different
            if value:
                self._run()
            else:
                self._stop()
            self._running = value

    def _run(self):
        pyatspi.Registry.registerEventListener(self._onMouseMoved, "mouse:abs")


    def _stop(self):
        pyatspi.Registry.deregisterEventListener(self._onMouseMoved, "mouse:abs")


    running = gobject.property(
        type=bool,
        nick='running',
        default=False,
        getter=_get_running,
        setter=_set_running)

    def _onMouseMoved(self, event):
        x, y = event.detail1, event.detail2
        freq, pan = self._calculateSoundParametersFromMousePosition(x, y)
        self._beep(freq, pan)

    def _calculateSoundParametersFromMousePosition(self, x, y):
        screen = gtk.gdk.screen_get_default()
        pan = 2 * (float(x) / screen.get_width())  -1
        freq = self.min_freq + (screen.get_height() - y) * (self.max_freq - self.min_freq) / screen.get_height()
        return (freq, pan)

    def _beep(self, frequency, panorama):
        self._player.set_state(gst.STATE_READY)
        self._source.set_property("freq", frequency)
        self._panorama.set_property("panorama", panorama)
        self._player.set_state(gst.STATE_PLAYING)

    def _onMessage(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self._player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self._player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "%s: %s" %(err, debug)


