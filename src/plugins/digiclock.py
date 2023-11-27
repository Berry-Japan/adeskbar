# adesk : "Clock" plugin

import gtk
import pango
import gobject
import time

import adesk.plugin as Plg

class Plugin(Plg.PluginContainer):
    def __init__(self, bar, settings):
        Plg.PluginContainer.__init__(self, bar, settings)
        self.can_zoom = False
        self.can_show_icon = False
        self.settings = settings
        self.bar = bar

        self.locked = False
        
        self.box = gtk.VBox(False, 0)
        self.box.set_border_width(0)
        self.add(self.box)

        self.set_from_config()

        self.update_time()
        gobject.timeout_add(1000, self.update_time)


    def set_from_config(self):
        self.time_txt = ''
        self.date_txt = ''
        self.lb_time = gtk.Label()
        self.lb_time.modify_font(pango.FontDescription(self.settings['time_font']))
        self.lb_time.set_use_markup(True)
        self.lb_time.set_alignment(0.5,0.5)
        self.box.pack_start(self.lb_time)

        if not self.settings['date'] == '':
            self.lb_date = gtk.Label()
            self.lb_date.modify_font(pango.FontDescription(self.settings['date_font']))
            self.lb_date.set_use_markup(True)
            self.lb_date.set_alignment(0.5,0.5)
            self.box.pack_start(self.lb_date)
        else:
            self.lb_date = None
        self.box.show_all()

    def update_time(self):
        if self.locked:
            return True
            
        now = time.localtime()
        time_current = time.strftime('<span color="%s">%s</span>' % (self.settings['time_color'], self.settings['time']), now)
        if self.lb_date:
            date_current = time.strftime('<span color="%s">%s</span>' % (self.settings['date_color'], self.settings['date']), now)

        if not time_current == self.time_txt:
            self.lb_time.set_markup(time_current)
            self.time_txt = time_current
            if self.lb_date:
                self.lb_date.set_markup(date_current)
                self.date_txt = date_current
        return True

    def resize(self):
        if self.bar.cfg['position']=='top' or self.bar.cfg['position']=='bottom':
            self.set_size_request(-1, self.cfg['icon_size'])
        else:
            self.set_size_request(self.cfg['icon_size'], -1)

    def restart(self):
        self.locked = True
        self.box.remove(self.lb_time)
        self.lb_time.destroy()
        if self.lb_date:
            self.box.remove(self.lb_date)
            self.lb_date.destroy()
        self.set_from_config()
        self.locked = False
        self.resize()
        self.update_time()
