# -*- coding: utf-8 -*-

##
#   ADesk Bar - UI
##

import gtk
import cairo
import gobject
import gmenu

import adesk.core as Core

def check_screen(widget):
    # To check if the display supports alpha channels, get the colormap
    screen = widget.get_screen()
    colormap = screen.get_rgba_colormap()
    if colormap == None:
        colormap = screen.get_rgb_colormap()
    # Now we have a colormap appropriate for the screen, use it
    widget.set_colormap(colormap)

class Window(gtk.Window):
    def __init__(self, wtype = gtk.WINDOW_TOPLEVEL):
        gtk.Window.__init__(self, wtype)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.stick()
        self.set_app_paintable(True)
        #~ self.set_double_buffered(False)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.ENTER_NOTIFY|gtk.gdk.LEAVE_NOTIFY)
        self.set_border_width(0)
        check_screen(self)

class TooltipWindow(Window):
    def __init__(self, bar, border = 4):
        Window.__init__(self, gtk.WINDOW_POPUP)
        self.connect('expose-event', self.expose)
        
        self.bar = bar
        self.cfg = bar.cfg
        self.tooltip_text = ''

        self.set_name("ADeskBarTooltipWindow")
        
        if self.is_composited():
            self.set_border_width(border)
        else:
            self.set_border_width(border)
            
        self.label = gtk.Label()
        self.add(self.label)
        self.label.show()

        self.timeout = None
        self.plugin = None

    def set_tooltip(self, text):
        self.label.set_text(text)

    def expose(self, widget, event):
        # On X11 this function returns whether a compositing
        # manager is running for the widget's screen
        
        if not self.is_composited():
            x, y, width, height = widget.get_allocation()
            bitmap = gtk.gdk.Pixmap(None, width, height, 1)
            cr = bitmap.cairo_create()
            # Clear the bitmap to False
            cr.set_source_rgb(0, 0, 0)
            cr.set_operator(cairo.OPERATOR_DEST_OUT)
            cr.paint()
            # Draw our shape into the bitmap using cairo
            cr.set_operator(cairo.OPERATOR_OVER)
            self.draw_shape(cr, x+1, y+1, width-2, height-2)
            self.shape_combine_mask(bitmap, 0, 0)
            
        ## Full transparent window
        cr = widget.window.cairo_create()
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        x, y, width, height = widget.get_allocation()
        self.draw_shape(cr, x+1, y+1, width-2, height-2)

    def draw_shape(self, cr, x, y, width, height, flag=False):
        r, g, b = self.cfg['bg_color_sub_rgb']
        
        if self.is_composited():
            opacity = 0.9
            radius = min(4, width/2, height/2)
        else:
            opacity = 1
            radius = 0

        cr.translate(x, y)

        #~ if self.cfg['bg_gradient']:
            #~ lg = cairo.LinearGradient(0, y, 0, y+height)
            #~ i = 0.0
            #~ while i <= 0.3:
#~ 
                #~ lg.add_color_stop_rgba(1-i, r-(i*r), g-(i*g), b-(i*b), opacity)
                #~ i += 0.1
            #~ i = 0.7
            #~ while i <= 1.0:
                #~ lg.add_color_stop_rgba(1-i, r-(1-i)*r, g-(1-i)*g, b-(1-i)*b, opacity)
                #~ i += 0.1
            #~ cr.set_source(lg)
        #~ else:
            #~ cr.set_source_rgba(r, g, b, opacity)

        cr.set_source_rgba(r, g, b, opacity)
        
        cr.move_to  (0, radius)
        cr.arc (radius, radius, radius, 3.14, 1.5 * 3.14)
        cr.line_to (width - radius, 0)
        cr.arc (width - radius, 0 + radius, radius, 1.5 * 3.14, 0.0)
        cr.line_to (width , height - radius)
        cr.arc (width - radius, height - radius, radius, 0.0, 0.5 * 3.14)
        cr.line_to (radius, height)
        cr.arc (radius, height - radius, radius, 0.5 * 3.14, 3.14)
        cr.close_path ()
        cr.fill()
        cr.save()

        cr.move_to  (0, radius)
        cr.arc (radius, radius, radius, 3.14, 1.5 * 3.14)
        cr.line_to (width - radius, 0)
        cr.arc (width - radius, 0 + radius, radius, 1.5 * 3.14, 0.0)
        cr.line_to (width , height - radius)
        cr.arc (width - radius, height - radius, radius, 0.0, 0.5 * 3.14)
        cr.line_to (radius, height)
        cr.arc (radius, height - radius, radius, 0.5 * 3.14, 3.14)
        cr.close_path ()

        r, g, b = self.cfg['border_color_sub_rgb']
        cr.set_source_rgba (r, g, b, opacity)
        cr.set_line_width(1)
        cr.stroke()
        cr.restore()

        return False

    def run(self, plugin):
        self.reposition(plugin)
        if len(plugin.tooltip) > 0:
            self.timeout = gobject.timeout_add(300, self.show_tooltip)
        self.plugin = plugin

    def show_tooltip(self):
        if not self.plugin.is_visible:
            self.set_tooltip(self.plugin.tooltip)
            self.show()
            self.reposition(self.plugin)
        return False

    def stop(self):
        if self.timeout:
            gobject.source_remove(self.timeout)
            self.timeout = None
        self.hide()
        self.plugin = None

    def reposition(self, plugin):
        self.resize(1, 1)
        offset_popup = 2
        plugin_x, plugin_y, plugin_w, plugin_h = plugin.get_allocation()
        window_x, window_y = self.bar.win.get_position()
        window_w, window_h = self.bar.win.get_size()
        (w, h) = self.get_size()
        x, y = 0, 0

        if self.bar.cfg['position'] == "top" or self.bar.cfg['position'] == "bottom":
            x = window_x + plugin_x - int( (w - self.bar.cfg['icon_size'])/2.0 )

            # check if window isn't out of screen
            if x < 5:
                x=5

            if self.bar.cfg['position'] == "top":
                y = window_y + window_h + offset_popup
            else:
                y = window_y - h - offset_popup

            while x >= 5 and x + w + 5 > gtk.gdk.screen_width():
                x = x - 1

        else:
            y = window_y + plugin_y

            if self.bar.cfg['position'] == "left":
                x = window_x + window_w + offset_popup
            else:
                x = window_x - w - offset_popup

            while y >= 0 and y + h > gtk.gdk.screen_height():
                y = y - 1

        self.move(x, y)
        #~ print 'move to :', x, y
        return False

class PopupWindow(Window):
    def __init__(self, bar, plugin, border = 4):
        Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        self.bar = bar
        self.cfg = bar.cfg
        self.plugin = plugin

        #~ self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        #~ self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        
        ## for debug
        #~ self.set_decorated(True)

        self.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
        self.connect('expose-event', self.expose)
        self.connect("focus-out-event", self.lost_focus)
        self.connect("key-press-event", self.onkeypress)
        self.connect('size-allocate', self._size_allocate)
        #~ self.set_name("ADeskBarPopupWindow")

        self.set_border_width(border)
        self.focus_check = False
        self.opener = None

    def _size_allocate(self, widget, allocation):
        self.reposition()

    def expose(self, widget, event):
        # On X11 this function returns whether a compositing
        # manager is running for the widget's screen
        if not self.is_composited():
            x, y, width, height = widget.get_allocation()
            bitmap = gtk.gdk.Pixmap(None, width, height, 1)
            cr = bitmap.cairo_create()
            # Clear the bitmap to False
            cr.set_source_rgb(0, 0, 0)
            cr.set_operator(cairo.OPERATOR_DEST_OUT)
            cr.paint()
            # Draw our shape into the bitmap using cairo
            cr.set_operator(cairo.OPERATOR_OVER)
            self.draw_shape(cr, x+1, y+1, width-2, height-2)
            self.shape_combine_mask(bitmap, 0, 0)
        
        #~ if self.is_composited():
        ## Full transparent window
        cr = widget.window.cairo_create()
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        ## Draw next over 'transparent window'
        cr.set_operator(cairo.OPERATOR_OVER)
        x, y, width, height = widget.get_allocation()
        self.draw_shape(cr, x+1, y+1, width-2, height-2)


    def draw_shape(self, cr, x, y, width, height, flag=False):
        r, g, b = self.cfg['bg_color_sub_rgb']

        if self.is_composited():
            opacity = 0.85
            radius = min(4, width/2, height/2)
        else:
            opacity = 1
            radius = 0

        cr.translate(x, y)
            
        cr.set_source_rgba(r, g, b, opacity)

        cr.move_to  (0, radius)
        cr.arc (radius, radius, radius, 3.14, 1.5 * 3.14)
        cr.line_to (width - radius, 0)
        cr.arc (width - radius, 0 + radius, radius, 1.5 * 3.14, 0.0)
        cr.line_to (width , height - radius)
        cr.arc (width - radius, height - radius, radius, 0.0, 0.5 * 3.14)
        cr.line_to (radius, height)
        cr.arc (radius, height - radius, radius, 0.5 * 3.14, 3.14)
        cr.close_path ()
        cr.fill()
        cr.save()

        cr.move_to  (0, radius)
        cr.arc (radius, radius, radius, 3.14, 1.5 * 3.14)
        cr.line_to (width - radius, 0)
        cr.arc (width - radius, 0 + radius, radius, 1.5 * 3.14, 0.0)
        cr.line_to (width , height - radius)
        cr.arc (width - radius, height - radius, radius, 0.0, 0.5 * 3.14)
        cr.line_to (radius, height)
        cr.arc (radius, height - radius, radius, 0.5 * 3.14, 3.14)
        cr.close_path ()

        r, g, b = self.cfg['border_color_sub_rgb']
        cr.set_source_rgba (r, g, b, opacity)
        cr.set_line_width(1)
        cr.stroke()
        cr.restore()

        return False

    def run(self):
        self.show()

    def reposition(self):
        offset_popup = 2
        offset_screen = 4
        plugin_x, plugin_y, plugin_w, plugin_h = self.plugin.get_allocation()

        window_x, window_y = self.bar.win.get_position()
        window_w, window_h = self.bar.win.get_size()
        p_x, p_y, w, h = self.get_allocation()
        x, y = 0, 0

        if self.bar.cfg['position'] == "top" or self.bar.cfg['position'] == "bottom":
            x = window_x + plugin_x - int( (w - self.bar.cfg['icon_size'])/2.0 )

            # check if window isn't out of screen
            if x < offset_screen:
                x=offset_screen

            if self.bar.cfg['position'] == "top":
                y = window_y + window_h + offset_popup
            else:
                y = window_y - h - offset_popup

            while x >= offset_screen and x + w + offset_screen > gtk.gdk.screen_width():
                x = x - 1

        else:
            y = window_y + plugin_y

            if self.bar.cfg['position'] == "left":
                x = window_x + window_w + offset_popup
            else:
                x = window_x - w - offset_popup

            while y >= 0 and y + h > gtk.gdk.screen_height():
                y = y - 1

        self.move(x, y)
        return False

    def open(self, widget = 0):
        if self.bar.opened_popup:
            if id(self) == id(self.bar.opened_popup):
                return
            self.bar.opened_popup.close()
        if type(widget) == type(1):
            self.x = widget
            self.y = widget
        else:
            self.opener = widget
            try:
                self.x = widget.allocation.x
                self.y = widget.allocation.y
            except:
                self.x = 0
                self.y = 0
                self.opener = None

        self.show()
        self.set_size_request(-1,-1)
        self.reposition()
        self.bar.opened_popup = self
        self.plugin.is_visible = True
        self.bar.can_hide = False

    def close(self):
        self.hide()
        self.plugin.is_visible = False
        try:
            self.opener.set_active(False)
        except:
            pass
            #~ raise
        self.bar.opened_popup = None
        self.bar.can_hide = True
        self.bar.bar_leave_notify()

    def toggle(self, widget=0):
        self.focus_check = False
        if self.bar.opened_popup:
            self.bar.opened_popup.focus_check = False
            if id(self) != id(self.bar.opened_popup):
                self.bar.opened_popup.close()
                self.open(widget)
                self.focus_check = True
                ## need this to give focus to window !
                self.present()
            else:
                self.close()
        else:
            self.open(widget)
            self.focus_check = True
            ## need this to give focus to window !
            self.present()
        self.bar.update()

    def lost_focus(self, widget, event):
        #~ print " ** lost_focus **"
        if self.focus_check:
            self.focus_check = False
            self.toggle(widget)

    def onkeypress(self, widget, event):
        ##FIXME!!
        return

        if event.keyval == gtk.keysyms.Escape:
            self.toggle(widget)

class Menu:
    
    def __init__(self, callback):
        
        self.callback = callback
        self.menu = gtk.Menu()
        
        ## Add Applications menu
        app_menu = gmenu.lookup_tree('applications.menu')
        if app_menu.root:
            self.add_to_menu(app_menu)

        ## Add Settings menu
        settings_menu = gmenu.lookup_tree('settings.menu')
        if settings_menu.root:

            separator = gtk.SeparatorMenuItem()
            self.menu.append(separator)
            separator.show()     
            self.add_to_menu(settings_menu)

    def add_to_menu(self, gmenu_tree):
        for m in gmenu_tree.root.contents:
            if m.get_type() == gmenu.TYPE_DIRECTORY:

                item = self.append_menu_item(self.menu, m.get_name(), m.get_icon(), None)
                submenu = gtk.Menu()
            
                for app in m.contents:
                    if app.get_type() == gmenu.TYPE_ENTRY:
                        sub_item = self.append_menu_item(submenu, app.get_name(), app.get_icon(), app.get_comment())
                        sub_item.connect("activate", self.callback, app)
                        sub_item.show()

                item.set_submenu(submenu)
                item.show()
                
            elif m.get_type() == gmenu.TYPE_SEPARATOR:
                separator = gtk.SeparatorMenuItem()
                self.menu.append(separator)
                separator.show() 

            elif m.get_type() == gmenu.TYPE_ENTRY:
                item = self.append_menu_item(self.menu, m.get_name(), m.get_icon(), m.get_comment())
                item.connect("activate", self.callback, m)
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

