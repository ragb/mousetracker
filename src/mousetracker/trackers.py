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

import pyatspi


class MousePositionTracker(object):
    """ Mouse locator class to locate the mouse using sound """

    def __init__(self, volume=1.0, min_freq=200, max_freq=1000):
        self._running = False
        
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

        self.volume = volume

        # properties
        self.min_freq = min_freq
        self.max_freq = max_freq

    def _get_volume(self):
        return self._source.get_property("volume")

    def _set_volume(self, volume):
        self._source.set_property("volume", volume)

    volume = property(_get_volume, _set_volume)

    def run(self):
        if self._running:
            return
        pyatspi.Registry.registerEventListener(self._onMouseMoved, "mouse:abs")
        self._running = True

    def stop(self):
        if not self._running:
            return
        pyatspi.Registry.deregisterEventListener(self._onMouseMoved, "mouse:abs")
        self._running = False

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


