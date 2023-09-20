import matplotlib
import mplfinance as fplt
import pandas_datareader as web
import talib

matplotlib.use("TkAgg")

#web.DataReader('^DJI', 'stooq')
#pd.read_csv("./resources/akcje.csv", delimiter='\t', header=None)
if __name__ == '__main__':

    lista = web.DataReader('KOM.PL', data_source='stooq', start="2010-01-01")[::-1]
    lista["RSI"] = talib.RSI(lista["Close"])
    print(lista)
    lista = lista

    chart = fplt.figure(style='charles',figsize=(6,7))
    ax1 = chart.add_subplot(3,1,(1,2))
    ax2 = chart.add_subplot(3,1,3, sharex=ax1)
    ap = [
        fplt.make_addplot(lista["RSI"], ax=ax2),
        fplt.make_addplot([20]*len(lista), ax=ax2),
        fplt.make_addplot([80]*len(lista), ax=ax2),
    ]
    fplt.plot(
        lista,
        type="candle",
        ax = ax1,
        addplot= ap
    )
    fplt.show()
