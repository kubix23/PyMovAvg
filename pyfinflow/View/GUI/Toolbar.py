import tkinter

from matplotlib.backends.backend_tkagg import (NavigationToolbar2Tk)


class Toolbar(NavigationToolbar2Tk):

    def __init__(self, canvas, window=None):
        super().__init__(canvas, window, pack_toolbar=False)
        self.state = False
        canvas.get_tk_widget().master.bind('<Key>', self.toggle)

    def toggle(self, event):
        if event.keysym == 'Alt_L':
            if self.state is True:
                self.pack_forget()
                self.state = False
            else:
                self.pack(fill=tkinter.X)
                self.state = True
