from pyfinflow.Scraper.ScrapData import Scrapdata


class PlotCollector:
    def __init__(self):
        self.models: [Scrapdata] = {}

    def getShares(self, name):
        if name in self.models:
            obj = self.models[name]
        else:
            self.models[name] = Scrapdata(name)
            obj = self.models[name]
        return obj.getData()
