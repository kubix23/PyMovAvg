import mplfinance as mpf
from matplotlib.widgets import MultiCursor

from Controler.PlotController import PlotController
from View.Plot.AnnotatedCursor import AnnotatedCursor
from View.Plot.ZoomPan import ZoomPan


class Quotes:
    def __init__(self, nrow, ncol):
        self.chart = None
        self.data = None
        self.size_row = nrow
        self.size_col = ncol
        self.main_ax = None
        self.controller = PlotController(self)

    def getChart(self):
        return self.chart

    def loadData(self, name):
        self.data = self.controller.getShares(name)
        self.data.to_csv("Data"+name+".csv")

    def plot(self, name=None):
        if name is not None:
            self.loadData(name)

        ap = self.calculateIndicators()
        self.chart, ax = mpf.plot(
            self.data,
            type="candle",
            addplot=ap,
            style='charles',
            returnfig=True,
            figsize=(self.size_row, self.size_col)
        )
        MultiCursor(self.chart.canvas, ax, color='r', lw=1,
                    horizOn=False, vertOn=True)
        self.main_ax = ax[0]
        ZoomPan(ax[0])
        AnnotatedCursor(
           y=self.data.Close.array,
           x=self.data.T.columns.array,
           textprops={'color': 'blue', 'fontweight': 'bold'},
           ax=ax[0],
           useblit=True,
           color='red',
           linewidth=2
        )


    def calculateIndicators(self):
        return [
            # mpf.make_addplot(None, panel=1),
            mpf.make_addplot([20] * len(self.data), panel=1),
            mpf.make_addplot([80] * len(self.data), panel=1),
        ]
