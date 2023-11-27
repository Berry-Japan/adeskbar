#!/usr/bin/python
import dbus
import sys
import gobject
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)
bus=dbus.SessionBus()

class DMenuClient(dbus.service.Object):
    def __init__(self):
        global bus
        bus_name = dbus.service.BusName('com.adcomp.adeskbar', bus=bus)
        dbus.service.Object.__init__(self, bus_name, '/com/adcomp/adeskbar')

    @dbus.service.method("com.adcomp.adeskbar")
    def get_result(self, result):
        global loop
        sys.stdout.write(result)
        loop.quit()

#~ main_lines = sys.stdin.readlines()

client = DMenuClient()

helloservice = bus.get_object('com.adcomp.adeskbar', '/com/adcomp/adeskbar')
show = helloservice.get_dbus_method('emit', 'com.adcomp.adeskbar')

if len(sys.argv) == 2:
    text = sys.argv[1]
else:
    text = "test DBUS"
    
print "emit DBUS message ... : ", text
show(text)

#~ loop = gobject.MainLoop()
#~ loop.run()
