from __future__ import annotations

import tkinter as tk
from tokenize import String

import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from pandas import DataFrame

from ..GUI.Toolbar import Toolbar
from ..Plot.Quotes import Quotation


class Window(tk.Tk):
    def __init__(self, data=None, screenName=None, baseName=None, className='Window',
                 useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.figure = None
        self.title("PyMovAvg")
        self.quotes = Quotation(7, 8)
        if data is not None:
            self.showData(data)

    def showData(self, data: DataFrame | None = None, name: String = None, plot_type="line", period=9):
        self.figure = self.quotes.plot(plot_type=plot_type, data_csv=data, name=name, period=period)
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        Toolbar(canvas, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def destroy(self):
        matplotlib.pyplot.close(self.figure)
        super().destroy()
