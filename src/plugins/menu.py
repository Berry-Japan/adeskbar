# -*- coding: utf-8 -*-

import gtk
import gmenu
import subprocess
import os

import adesk.plugin as Plg
import adesk.core as Core
import adesk.ui 

M_APPLICATIONS = gmenu.lookup_tree('applications.menu')
M_SETTINGS = gmenu.lookup_tree('settings.menu')


class Plugin(Plg.Plugin):
    def __init__(self, bar, settings):
        Plg.Plugin.__init__(self, bar, settings)
        self.settings = settings
        self.bar = bar
        self.can_zoom = True
        self.menu = adesk.ui.Menu(self.launch_app)

    def onClick(self, widget, event):

        def get_position(menu):
            plugin_x, plugin_y, plugin_w, plugin_h = self.get_allocation()
            screen_width, screen_height =  gtk.gdk.screen_width(), gtk.gdk.screen_height()
            menu_size = self.menu.menu.size_request()

            padding = 0
            orientation = self.bar.cfg['position']
            
            if orientation == "bottom":
                icon_y = self.bar.bar_pos_y  - menu_size[1] - padding
                icon_x = self.bar.bar_pos_x + plugin_x
            elif orientation == "top":
                icon_y = self.bar.bar_pos_y + self.bar.draw_height + padding
                icon_x = self.bar.bar_pos_x + plugin_x
            elif orientation == "right":
                icon_x = self.bar.bar_pos_x - menu_size[0] - padding
                icon_y = self.bar.bar_pos_y + plugin_y
            elif orientation == "left":
                icon_x = self.bar.bar_pos_x + self.bar.draw_width + padding
                icon_y = self.bar.bar_pos_y + plugin_y

            # Make sure the bottom of the menu doesn't get below the bottom of the screen
            icon_y = min(icon_y, screen_height - menu_size[1])

            return (icon_x, icon_y, False)
        self.menu.menu.popup(None, None, get_position, 0, 0)


    def resize(self):
        self.set_size_request(self.cfg['icon_size'], self.cfg['icon_size'])

    def launch_app(self, widget, menu_item):
        # Strip last part of path if it contains %<a-Z>
        command = menu_item.exec_info.split('%')[0]
        if menu_item.launch_in_terminal:
            command = 'x-terminal-emulator -e %s' % command
        Core.launch_command(command)

class Menu:
    def __init__(self):
        self.menu = gtk.Menu()
        
        ## Add Applications menu
        self.add_to_menu(M_APPLICATIONS)
   
        separator = gtk.SeparatorMenuItem()
        self.menu.append(separator)
        separator.show()     

        ## Add Settings menu
        self.add_to_menu(M_SETTINGS)

    def add_to_menu(self, gmenu_tree):

        for m in gmenu_tree.root.contents:
            if m.get_type() == gmenu.TYPE_DIRECTORY:

                item = self.append_menu_item(self.menu, m.get_name(), m.get_icon(), None)
                submenu = gtk.Menu()
            
                for app in m.contents:
                    if app.get_type() == gmenu.TYPE_ENTRY:
                        sub_item = self.append_menu_item(submenu, app.get_name(), app.get_icon(), app.get_comment())
                        if app.launch_in_terminal:
                            exec_info = 'x-terminal-emulator -e %s' % app.exec_info
                        else:
                            exec_info = app.exec_info
                        sub_item.connect("activate", self.launch_app, exec_info)
                        sub_item.show()

                item.set_submenu(submenu)
                item.show()
                
            elif m.get_type() == gmenu.TYPE_SEPARATOR:
                separator = gtk.SeparatorMenuItem()
                self.menu.append(separator)
                separator.show() 

            elif m.get_type() == gmenu.TYPE_ENTRY:
                item = self.append_menu_item(self.menu, m.get_name(), m.get_icon(), m.get_comment())
                item.connect("activate", self.launch_app, m.exec_info)
                item.show()

    def create_menu_item(self, label, icon_name, comment):
        item = gtk.ImageMenuItem(label)

        if gtk.gtk_version >= (2, 16, 0):
            item.props.always_show_image = True
            
        icon_pixbuf = Core.get_pixbuf_icon(icon_name)
        item.set_image(gtk.image_new_from_pixbuf(icon_pixbuf))
        
        if comment is not None:
            item.set_tooltip_text(comment)
        return item

    def append_menu_item(self, menu, label, icon_name, comment):
        item = self.create_menu_item(label, icon_name, comment)
        menu.append(item)
        return item

    def launch_app(self, widget, exec_info):
        # Strip last part of path if it contains %<a-Z>
        command = exec_info.split('%')[0]
        Core.launch_command(command)
