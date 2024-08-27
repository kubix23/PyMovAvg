from __future__ import annotations

import tkinter as tk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

from View.GUI.Toolbar import Toolbar
from View.Plot.Quotes import Quotes


class Window(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className='Window',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Matplotlib in Tkinter")
        self.quotes = Quotes(7, 8)
        self.quotes.loadData("MAB")
        self.quotes.plot()
        canvas = FigureCanvasTkAgg(self.quotes.getChart(), master=self)

        Toolbar(canvas, self)

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        tk.mainloop()
