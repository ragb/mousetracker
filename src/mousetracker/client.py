import dbus
import trackers, daemon

class TrackerPropertiesClient(dbus.Interface):

    def __init__(self, object_path=None):
        if not object_path and not self.remote_object_path:
            raise AttributeError, "no object path specified in constructor nor in class"
        if not object_path:
            object_path = self.remote_object_path
        bus = dbus.SessionBus()
        bus_name = daemon.BUS_NAME
        proxy = bus.get_object(bus_name, object_path)
        dbus.Interface.__init__(self, proxy, trackers.MouseTracker.PROPERTIES_IFACE)

class MousePositionTrackerPropertiesClient(TrackerPropertiesClient):
    remote_object_path = trackers.MousePositionTracker.object_path
