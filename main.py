import matplotlib

from src.View.GUI.Window import Window

matplotlib.use("TkAgg")

# web.DataReader('^DJI', 'stooq')
# pd.read_csv("./resources/akcje.csv", delimiter='\t', header=None)
if __name__ == '__main__':
    Window()
