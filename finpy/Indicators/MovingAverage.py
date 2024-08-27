from Indicators.Indicator import Indicator


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
            alpha = 2 / (period + 1)
            initial = data_calc[0]
            ema = [initial]
            for price in data_calc[1:]:
                ema.append((price - ema[-1])*alpha+ema[-1])
            return ema


