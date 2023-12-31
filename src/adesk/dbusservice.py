# -*- coding: utf-8 -*-

# Author: Milan Nikolic <gen2brain@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

class DBusService(dbus.service.Object):
    """ DBus Service """

    def __init__(self, main_instance):
        """ Constructor """
        print "Start DBUS main loop ............."
        loop = DBusGMainLoop()
        self.main = main_instance
        session_bus = dbus.SessionBus(mainloop=loop)
        bus_name = dbus.service.BusName('com.adcomp.adeskbar', bus=session_bus)
        dbus.service.Object.__init__(self, bus_name, '/com/adcomp/adeskbar')

        obj = session_bus.get_object('com.adcomp.adeskbar', '/com/adcomp/adeskbar')
        iface = dbus.Interface(obj, 'com.adcomp.adeskbar')
        iface.connect_to_signal("signal", self.signal_handler)

    @dbus.service.signal('com.adcomp.adeskbar', signature='s')
    def signal(self, signal):
        """ DBus signal """
        #~ print " DBus signal "
        pass

    @dbus.service.method('com.adcomp.adeskbar', in_signature='s', out_signature='')
    def emit(self, signal):
        """ DBus method to emit signal """
        #~ print " DBus method to emit signal "
        self.signal(signal)

    def signal_handler(self, signal):
        """ Handle dbus signals and pass them to main app """
        print "dbus signal :", signal
        
        if signal == 'toggle_hidden':
            self.main.toggle_hidden()

