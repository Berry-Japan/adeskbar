# -*- coding: utf-8 -*-

import gtk

settings = {
    'time':'%H:%M', 'time_color':'#EEEEEE', 'time_font':'Sans Bold 12',
    'date':'%d/%m', 'date_color':'#B5B5B5', 'date_font':'Sans Bold 8',
    }

INFO = """%a  Locale’s abbreviated weekday name.
%A  Locale’s full weekday name.
%b  Locale’s abbreviated month name.
%B  Locale’s full month name.
%c  Locale’s appropriate date and time representation.
%d  Day of the month as a decimal number [01,31].
%H  Hour (24-hour clock) as a decimal number [00,23].
%I  Hour (12-hour clock) as a decimal number [01,12].
%j  Day of the year as a decimal number [001,366].
%m  Month as a decimal number [01,12].
%M  Minute as a decimal number [00,59].
%p  Locale’s equivalent of either AM or PM.     (1)
%S  Second as a decimal number [00,61].     (2)
%U  Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
    All days in a new year preceding the first Sunday are considered to be in week 0.   (3)
%w  Weekday as a decimal number [0(Sunday),6].
%W  Week number of the year (Monday as the first day of the week) as a decimal number [00,53].
    All days in a new year preceding the first Monday are considered to be in week 0.   (3)
%x  Locale’s appropriate date representation.
%X  Locale’s appropriate time representation.
%y  Year without century as a decimal number [00,99].
%Y  Year with century as a decimal number.
%Z  Time zone name (no characters if no time zone exists).
%%  A literal '%' character.

Notes:

1. the %p directive only affects the output hour field if the %I directive is used to parse the hour.

2. The range really is 0 to 61; this accounts for leap seconds and the (very rare) double leap seconds.

3. %U and %W are only used in calculations when the day of the week and the year are specified.
"""

class config(gtk.Frame):
    def __init__(self, conf, ind):
        gtk.Frame.__init__(self)
        self.conf = conf
        self.ind = ind

        self.set_border_width(5)
        framebox = gtk.VBox(False, 0)
        framebox.set_border_width(5)
        framebox.set_spacing(10)
        self.add(framebox)

        for key in settings:
            if not conf.launcher[ind].has_key(key):
                conf.launcher[ind][key] = settings[key]

        self.settings = conf.launcher[ind]

        table = gtk.Table(4, 2, False)

        label = gtk.Label("Time :")
        label.set_alignment(0, 0.5)
        self.time_format = gtk.Entry()
        self.time_format.set_width_chars(10)
        self.time_format.set_text(self.settings['time'])

        map = label.get_colormap()
        colour = map.alloc_color(self.settings['time_color'])
        self.time_color = gtk.ColorButton(colour)
        self.time_font = gtk.FontButton(self.settings['time_font'])

        table.attach(label, 0, 1, 0, 1)
        table.attach(self.time_format, 1, 2, 0, 1)
        table.attach(self.time_color, 2, 3, 0, 1)
        table.attach(self.time_font, 3, 4, 0, 1)

        label = gtk.Label("Date :")
        label.set_alignment(0, 0.5)
        self.date_format = gtk.Entry()
        self.date_format.set_width_chars(10)
        self.date_format.set_text(self.settings['date'])

        colour = map.alloc_color(self.settings['date_color'])
        self.date_color = gtk.ColorButton(colour)
        self.date_font = gtk.FontButton(self.settings['date_font'])

        table.attach(label, 0, 1, 1, 2)
        table.attach(self.date_format, 1, 2, 1, 2)
        table.attach(self.date_color, 2, 3, 1, 2)
        table.attach(self.date_font, 3, 4, 1, 2)

        framebox.pack_start(table, True)

        text_timeformat = gtk.TextView()
        text_timeformat.set_wrap_mode(gtk.WRAP_WORD)
        text_timeformat.set_border_width(2)
        buffer = text_timeformat.get_buffer()
        buffer.set_text(INFO)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(text_timeformat)

        expander = gtk.expander_new_with_mnemonic("_Info")
        expander.add(sw)
        framebox.pack_start(expander, True)

    def save_change(self):
        self.conf.launcher[self.ind]['time'] = self.time_format.get_text()
        self.conf.launcher[self.ind]['time_color'] = gtk.color_selection_palette_to_string([self.time_color.get_color()])
        self.conf.launcher[self.ind]['time_font'] = self.time_font.get_font_name()
        self.conf.launcher[self.ind]['date'] = self.date_format.get_text()
        self.conf.launcher[self.ind]['date_color'] = gtk.color_selection_palette_to_string([self.date_color.get_color()])
        self.conf.launcher[self.ind]['date_font'] = self.date_font.get_font_name()
        self.conf.plg_mgr.plugins[self.ind].restart()
