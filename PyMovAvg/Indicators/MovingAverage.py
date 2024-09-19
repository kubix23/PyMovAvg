from .Indicator import Indicator


class MovingAverage(Indicator):
    @staticmethod
    def calculate(data, column, period=5, type='SMA'):
        if type not in ['SMA', 'WMA', 'EMA']:
            return None
        data_calc = data[column]
        if type == 'SMA':
            return data_calc.rolling(window=period).mean()
        elif type == 'WMA':
            return data_calc.rolling(window=period).apply(lambda x: x[::-1].cumsum().sum() * 2 / period / (period + 1))
        elif type == 'EMA':
            return data_calc.ewm(span=period, adjust=False).mean()


