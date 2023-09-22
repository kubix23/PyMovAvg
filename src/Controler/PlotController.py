from Model.ScrapData import Scrapdata


class PlotController:
    def __init__(self, view):
        self.models: [Scrapdata] = {}
        self.view = view

    def getShares(self, name):
        if name in self.models:
            obj = self.models[name]
        else:
            self.models[name] = Scrapdata(name)
            obj = self.models[name]
        return obj.getData()
