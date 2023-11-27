# -*- coding: utf-8 -*-

import gtk

settings = { 
    'desktop_color':'#EEEEEE', 'desktop_font':'Sans Bold 12',
    'show_desk_pos':1, 'show_desk_name':0, 'show_all_win':1
    }

class config(gtk.Frame):
    def __init__(self, conf, ind):
        gtk.Frame.__init__(self)
        self.conf = conf
        self.ind = ind
        
        self.settings = conf.launcher[ind]

        self.set_border_width(5)
        framebox = gtk.VBox(False, 0)
        framebox.set_border_width(5)
        framebox.set_spacing(10)
        self.add(framebox)

        for key in settings:
            if not self.settings.has_key(key):
                self.settings[key] = settings[key]

        self.show_all_win_checkbox = gtk.CheckButton('Show all windows')
        self.show_all_win_checkbox.set_active(int(self.settings['show_all_win']))
        framebox.pack_start(self.show_all_win_checkbox, True)

        self.show_desk_pos_checkbox = gtk.CheckButton('Show desktop position')
        self.show_desk_pos_checkbox.set_active(int(self.settings['show_desk_pos']))
        framebox.pack_start(self.show_desk_pos_checkbox, True)


        self.show_desk_name_checkbox = gtk.CheckButton('Show desktop name')
        self.show_desk_name_checkbox.set_active(int(self.settings['show_desk_name']))
        
        label = gtk.Label('   ')
        map = label.get_colormap()

        colour = map.alloc_color(self.settings['desktop_color'])
        self.desk_color = gtk.ColorButton(colour)
        self.desk_font = gtk.FontButton(self.settings['desktop_font'])

        
        
        optionbox = gtk.HBox(False, 0)
        optionbox.set_border_width(0)
        optionbox.set_spacing(10)
        
        optionbox.pack_start(label, False)
        optionbox.pack_start(self.show_desk_name_checkbox, True)
        
        framebox.pack_start(optionbox, True)

        optionbox = gtk.HBox(False, 0)
        optionbox.set_border_width(0)
        optionbox.set_spacing(10)

        optionbox.pack_start(self.desk_font, True)
        optionbox.pack_start(self.desk_color, False)
        framebox.pack_start(optionbox, True)

    def save_change(self):
        self.settings['desktop_color'] = gtk.color_selection_palette_to_string([self.desk_color.get_color()])
        self.settings['desktop_font'] = self.desk_font.get_font_name()
        self.settings['show_desk_pos'] = int(self.show_desk_pos_checkbox.get_active())
        self.settings['show_desk_name'] = int(self.show_desk_name_checkbox.get_active())
        self.settings['show_all_win'] = int(self.show_all_win_checkbox.get_active())
        self.conf.plg_mgr.plugins[self.ind].restart()
