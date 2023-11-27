import gtk

settings = {'terminal':'terminator'}

class config(gtk.Frame):
    def __init__(self, conf, ind):
        gtk.Frame.__init__(self)
        self.conf = conf
        self.ind = ind

        self.set_border_width(5)
        framebox = gtk.HBox(False, 0)
        framebox.set_border_width(5)
        framebox.set_spacing(10)
        self.add(framebox)

        for key in settings:
            if not conf.launcher[ind].has_key(key):
                conf.launcher[ind][key] = settings[key]

        self.settings = conf.launcher[ind]

        label = gtk.Label("Terminal :")
        label.set_alignment(0, 0.5)
        self.terminal = gtk.Entry()
        self.terminal.set_width_chars(20)
        self.terminal.set_text(conf.launcher[ind]['terminal'])

        framebox.pack_start(label)
        framebox.pack_end(self.terminal)

    def save_change(self):
        self.conf.launcher[self.ind]['terminal'] = self.terminal.get_text()

