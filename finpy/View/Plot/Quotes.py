import mplfinance as mpf
from matplotlib.widgets import MultiCursor

from Indicators.MovingAverage import MovingAverage
from finpy.Scraper.PlotCollector import PlotCollector
from finpy.View.Plot.AnnotatedCursor import AnnotatedCursor
from finpy.View.Plot.ZoomPan import ZoomPan


class Quotation:
    def __init__(self, nrow, ncol):
        self.chart = None
        self.data = None
        self.size_row = nrow
        self.size_col = ncol
        self.main_ax = None
        self.col = PlotCollector()

    def getChart(self):
        return self.chart

    def loadDataByName(self, name):
        self.data = self.col.getShares(name)

    def loadDataByFile(self, data_csv):
        self.data = data_csv

    def plot(self, name=None, data_csv=None):
        if name is not None:
            self.loadDataByName(name)
        elif data_csv is not None:
            self.loadDataByName(name)

        if self.data is not None:
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
            mpf.make_addplot(MovingAverage.calculate(self.data, 'Open', type='SMA'), panel=0),
            mpf.make_addplot(MovingAverage.calculate(self.data, 'Open', type='WMA'), panel=0),
            mpf.make_addplot(MovingAverage.calculate(self.data, 'Open', type='EMA'), panel=0),
            mpf.make_addplot([20] * len(self.data), panel=1),
            mpf.make_addplot([80] * len(self.data), panel=1),
        ]


