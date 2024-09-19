import pandas_datareader as web

class Scrapdata:
    def __init__(self, name):
        self.data = web.DataReader(name, data_source='stooq')[::-1]

    def getData(self):
        return self.data
