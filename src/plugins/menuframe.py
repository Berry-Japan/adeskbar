# -*- coding: utf-8 -*-

import gtk
import gmenu

import adesk.plugin as Plg
import adesk.ui as UI
import adesk.core as Core

MENU_WIDTH = 400

class Plugin(Plg.Plugin):
    def __init__(self, bar, settings):
        Plg.Plugin.__init__(self, bar, settings)
        self.bar = bar
        self.settings = settings
        self.can_zoom = True
        self.menu = Menu_UI(self, bar)

    def onClick(self, widget, event):
        self.menu.toggle(self.menu)

    def resize(self):
        self.set_size_request(self.cfg['icon_size'], self.cfg['icon_size'])

class Menu_UI(UI.PopupWindow):
    def __init__(self, plugin, bar):
        UI.PopupWindow.__init__(self, bar, plugin)
        self.set_size_request(MENU_WIDTH,-1)

        self.nbook = gtk.Notebook()
        self.nbook.set_tab_pos(gtk.POS_LEFT)
        self.nbook.set_border_width(0)
        self.nbook.show()
        self.add(self.nbook)
        #~ terminal = plugin.settings['terminal']
        terminal = 'x-terminal-emulator'
        
        self.create_menu()

    def executeAction(self, widget, event, app):
        if event.button == 1: # left click
            command = app.exec_info.split('%')[0]
            if app.launch_in_terminal:
                command = 'x-terminal-emulator -e %s' % command
            Core.launch_command(command)
            self.toggle()

    def create_menu(self):
        menu_tree = gmenu.lookup_tree('applications.menu')
        self.add_to_nbook(menu_tree)
        menu_tree = gmenu.lookup_tree('settings.menu')
        self.add_to_nbook(menu_tree)
        
    def add_to_nbook(self, menu_tree):
        for m in menu_tree.root.contents:
            if m.get_type() == gmenu.TYPE_DIRECTORY:
                box = self.make_tab_box(m.get_name(), m.get_icon())
                for app in m.contents:
                    if app.get_type() == gmenu.TYPE_ENTRY:
                        button = Core.image_button(app.get_name(), app.get_icon(), 24)
                        button.set_tooltip_text(app.get_comment())
                        button.connect("button-release-event", self.executeAction, app)
                        box.pack_start(button, False, False)

    def make_tab_box(self, label, icon):
        box = gtk.VBox()
        box.show()
        box.set_spacing(1)
        box.set_border_width(1)

        scrolled = gtk.ScrolledWindow()
        scrolled.show()
        scrolled.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrolled.add_with_viewport(box)

        tab_box = gtk.HBox(False, 4)
        tab_label = gtk.Label(label)
        tab_icon = gtk.Image()
        tab_icon.set_from_icon_name(icon, 24)

        tab_box.pack_start(tab_icon, False)
        tab_box.pack_start(tab_label, False)

        # needed, otherwise even calling show_all on the notebook won't
        # make the hbox contents appear.
        tab_box.show_all()
        self.nbook.append_page(scrolled, tab_box)
        return box
