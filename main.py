import matplotlib
import pandas_datareader as web
import pandas as pd
import talib
import mplfinance as fplt
matplotlib.use("TkAgg")

#web.DataReader('^DJI', 'stooq')
#pd.read_csv("./resources/akcje.csv", delimiter='\t', header=None)
if __name__ == '__main__':
    lista = web.DataReader('^DJI', 'stooq')[::-1]
    lista["RSI"] = talib.RSI(lista["Close"])
    print(lista)
    lista = lista.tail(30)
    rsi = fplt.make_addplot(lista["RSI"],secondary_y=True)

    chart = fplt.figure(style='charles',figsize=(7,8))
    ax1 = chart.add_subplot(2,1,1)
    ax2 = chart.add_subplot(2,1,2)
    fplt.plot(
        lista,
        type="candle",
        ax = ax1,
        volume=ax2
    )
    fplt.show()
