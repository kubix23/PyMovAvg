import pandas_datareader as web

class Scrapdata:
    def __init__(self, name):
        self.data = web.DataReader("{}.PL".format(name), data_source='stooq', start="2010-01-01")[::-1]

    def getData(self):
        return self.data
