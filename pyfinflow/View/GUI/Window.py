from __future__ import annotations

import tkinter as tk

import matplotlib
import matplotlib.pyplot
import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

from pyfinflow.View.GUI.Toolbar import Toolbar
from pyfinflow.View.Plot.Quotes import Quotation


class Window(tk.Tk):
    def __init__(self,data=None, screenName=None, baseName=None, className='Window',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title("Matplotlib in Tkinter")
        self.quotes = Quotation(7, 8)
        if data is not None:
            self.showData(data)

    def showData(self, data=None):
        self.quotes.plot(data_csv=data)
        canvas = FigureCanvasTkAgg(self.quotes.getChart(), master=self)
        Toolbar(canvas, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.mainloop()

    def destroy(self):
        matplotlib.pyplot.close(self.quotes.figure)
        super().destroy()
