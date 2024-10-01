import mplfinance as mpf
from pandas import DataFrame

from ...Indicators.MovingAverage import MovingAverage
from ...Scraper.PlotCollector import PlotCollector
from .AnnotatedCursor import AnnotatedCursor
from .ZoomPan import ZoomPan


class Quotation:
    def __init__(self, nrow, ncol):
        self.zoom_pan = None
        self.data: DataFrame | None = None
        self.size_row = nrow
        self.size_col = ncol
        self.main_ax = None
        self.prepare_data = None
        self.col = PlotCollector()
        self.cursor = None

    def getChart(self):
        return self.figure

    def loadDataByName(self, name):
        self.data = self.col.getQuotes(name)

    def loadDataByFile(self, data_csv):
        self.data = data_csv
        self.prepare_data = self.prepareData(self.data)

    def prepareData(self, data: DataFrame):
        temp = data.copy()
        if 'Close' not in temp.columns:
            temp['Close'] = temp.iloc[:,0]
        if 'Open' not in temp.columns:
            temp['Open'] = temp['Close']
        if 'Low' not in temp.columns:
            temp['Low'] = temp['Close']
        if 'High' not in temp.columns:
            temp['High'] = temp['Close']
        return temp

    def plot(self, plot_type="line", name=None, data_csv=None, period=9):
        if name is not None:
            self.loadDataByName(name)
        elif data_csv is not None:
            self.loadDataByFile(data_csv)
        if self.data is not None:
            indicators = self.calculateIndicators(period)
            figure, axes = mpf.plot(
                self.prepare_data,
                type=plot_type,
                addplot=self.addPlots([i["Data"] for i in indicators], period),
                style='charles',
                figsize=(self.size_row, self.size_col),
                ylabel="",
                returnfig=True
            )
            self.main_ax = axes[0]
            self.main_ax.yaxis.set_label_position("left")
            self.main_ax.yaxis.tick_left()
            for i in indicators:
                self.data[i["Name"]] = i["Data"]
            self.cursor = AnnotatedCursor(self.data,
                                          self.main_ax,
                                          useblit=True,
                                          color='r',
                                          lw=1,
                                          horizOn=False,
                                          vertOn=True
                                          )
            self.zoom_pan = ZoomPan(figure, axes, useblit=True)
            return figure

    def calculateIndicators(self, period=9):
        return [
            {"Data": MovingAverage.calculate(self.prepare_data, period=period, column='Close', type='SMA'), "Name": "SMA"},
            {"Data": MovingAverage.calculate(self.prepare_data, period=period, column='Close', type='WMA'), "Name": "WMA"},
            {"Data": MovingAverage.calculate(self.prepare_data, period=period, column='Close', type='EMA'), "Name": "EMA"}
        ]

    def addPlots(self, data, period=9):
        return [
            mpf.make_addplot(
                data[0], panel=0,
                label="SMA {}".format(period)
            ),
            mpf.make_addplot(
                data[1], panel=0,
                label="WMA {}".format(period)
            ),
            mpf.make_addplot(
                data[2], panel=0,
                label="EMA {}".format(period)
            ),
        ]
