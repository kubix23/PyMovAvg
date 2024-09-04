import mplfinance as mpf
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import MultiCursor, Cursor

from Indicators.MovingAverage import MovingAverage
from PyMovePlot.Scraper.PlotCollector import PlotCollector
from PyMovePlot.View.Plot.AnnotatedCursor import AnnotatedCursor
from PyMovePlot.View.Plot.ZoomPan import ZoomPan


class Quotation:
    def __init__(self, nrow, ncol):
        self.zoom_pan = None
        self.figure = None
        self.data = None
        self.size_row = nrow
        self.size_col = ncol
        self.main_ax = None
        self.col = PlotCollector()
        self.cursor = None

    def getChart(self):
        return self.figure

    def loadDataByName(self, name):
        self.data = self.col.getShares(name)

    def loadDataByFile(self, data_csv):
        self.data = data_csv

    def plot(self, name=None, data_csv=None):
        if name is not None:
            self.loadDataByName(name)
        elif data_csv is not None:
            self.loadDataByFile(data_csv)
        if self.data is not None:
            ap = self.calculateIndicators()

            self.figure, axes = mpf.plot(
                self.data,
                type="candlestick",
                addplot=ap,
                style='charles',
                figsize=(self.size_row, self.size_col),
                returnfig=True
            )
            self.main_ax = axes[0]
            self.cursor = AnnotatedCursor(self.data, self.main_ax, useblit=True, color='r', lw=1, horizOn=False, vertOn=True)
            self.zoom_pan = ZoomPan(self.figure, axes, self.data)


    def calculateIndicators(self):
        return [
            mpf.make_addplot(MovingAverage.calculate(self.data, 'Open', type='SMA'), panel=0, label="SMA"),
            mpf.make_addplot(MovingAverage.calculate(self.data, 'Open', type='WMA'), panel=0, label="WMA"),
            mpf.make_addplot(MovingAverage.calculate(self.data, 'Open', type='EMA'), panel=0, label="EMA"),
        ]
