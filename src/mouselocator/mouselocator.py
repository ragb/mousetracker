#! /usr/bin/env python

import pygtk
pygtk.require("2.0")

import gobject
import gtk
import pyatspi

import pygst
pygst.require("0.10")

import gst



class MouseSoundLocator(object):
    """ Mouse locator class to locate the mouse using sound """

    def __init__(self):
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
        freq = 200 + (screen.get_height() - y) * 1000 / screen.get_height()
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


class Application(object):

    def __init__(self):
        pass


    def main(self, argv):

    # setup signal handlers
        import signal
        signal.signal(signal.SIGINT, lambda signum, stackframe : self.quit())

        # startup sound locator
        self._locator = MouseSoundLocator()
        self._locator.run()
        pyatspi.Registry.start()

    def quit(self):
        self._locator.stop()
        pyatspi.Registry.stop()

if __name__ == '__main__':
    import sys
    Application().main(sys.argv)
