from __future__ import annotations

import tkinter as tk

import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

from pyfinflow.View.GUI.Toolbar import Toolbar
from pyfinflow.View.Plot.Quotes import Quotation


class Window(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className='Window',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Matplotlib in Tkinter")
        self.quotes = Quotation(7, 8)
        self.quotes.plot("MAB")
        canvas = FigureCanvasTkAgg(self.quotes.getChart(), master=self)

        Toolbar(canvas, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.mainloop()

    def loadData(self, data):
        self.quotes.loadDataByFile(data)

    def destroy(self):
        matplotlib.pyplot.close(self.quotes.chart)
        super().destroy()
