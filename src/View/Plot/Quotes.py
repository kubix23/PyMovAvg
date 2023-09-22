import mplfinance as fplt
import talib

from Controler.PlotController import PlotController
from View.Plot.ZoomPan import ZoomPan


class Quotes:
    def __init__(self, nrow, ncol):
        self.controller = PlotController(self)
        self.data = None
        self.chart = fplt.figure(style='charles', figsize=(nrow, ncol))
        self.loadData("PGE")
        ax1 = self.chart.add_subplot(3, 1, (1, 2))
        ax2 = self.chart.add_subplot(3, 1, 3, sharex=ax1)
        zp = ZoomPan()
        zp.zoom_factory(ax1)
        zp.pan_factory(ax1)

        ap = self.calculateIndicators(ax2)

        fplt.plot(
            self.data,
            type="candle",
            ax=ax1,
            addplot=ap
        )

    def getChart(self):
        return self.chart

    def loadData(self, name):
        self.data = self.controller.getShares(name)

    def calculateIndicators(self, plot):
        return [
            fplt.make_addplot(talib.RSI(self.data["Close"]), ax=plot),
            fplt.make_addplot([20] * len(self.data), ax=plot),
            fplt.make_addplot([80] * len(self.data), ax=plot),
        ]
