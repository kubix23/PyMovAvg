import numpy as np
from matplotlib.widgets import Cursor


class AnnotatedCursor(Cursor):
    def __init__(self, x, y, textprops=None, **cursorargs):
        if textprops is None:
            textprops = {}
        self.x_data = x
        self.y_data = y
        self.numberformat = "{0:.4g};{1:.4g}"
        self.offset = np.array((5, 5))
        self.dataaxis = 'x'

        super().__init__(**cursorargs)

        self.set_position(0, self.y_data[0])
        self.text = self.ax.text(
            self.ax.get_xbound()[0],
            self.ax.get_ybound()[0],
            "0, 0",
            animated=bool(self.useblit),
            visible=False, **textprops)
        self.lastdrawnplotpoint = None

    def onmove(self, event):
        if self.ignore(event):
            self.lastdrawnplotpoint = None
            return
        if not self.canvas.widgetlock.available(self):
            self.lastdrawnplotpoint = None
            return

        if event.inaxes != self.ax:
            self.lastdrawnplotpoint = None
            self.text.set_visible(False)
            super().onmove(event)
            return

        plotpoint = None
        if event.xdata is not None and event.ydata is not None:
            plotpoint = self.set_position(event.xdata, event.ydata)
            if plotpoint is not None:
                event.xdata = plotpoint[0]
                event.ydata = plotpoint[1]

        if plotpoint is not None and plotpoint == self.lastdrawnplotpoint:
            return

        super().onmove(event)

        if not self.get_active() or not self.visible:
            return

        if plotpoint is not None:
            temp = [event.xdata, event.ydata]
            temp = self.ax.transData.transform(temp)
            temp = temp + self.offset
            temp = self.ax.transData.inverted().transform(temp)
            self.text.set_position(temp)
            self.text.set_text(self.numberformat.format(*plotpoint))
            self.text.set_visible(self.visible)
            self.needclear = True
            self.lastdrawnplotpoint = plotpoint
        else:
            self.text.set_visible(False)


        if self.useblit:
            self.ax.draw_artist(self.text)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()

    def set_position(self, xpos, ypos):
        xdata = self.x_data
        ydata = self.y_data

        if self.dataaxis == 'x':
            pos = xpos
            data = xdata
            lim = self.ax.get_xlim()
        elif self.dataaxis == 'y':
            pos = ypos
            data = ydata
            lim = self.ax.get_ylim()
        else:
            raise ValueError(f"The data axis specifier {self.dataaxis} should "
                             f"be 'x' or 'y'")

        if pos is not None and lim[0] <= pos <= lim[1]:
            index = np.searchsorted(data, pos)
            if index < 0 or index >= len(data):
                return None
            return (xdata[index], ydata[index])

        return None

    def clear(self, event):
        super().clear(event)
        if self.ignore(event):
            return
        self.text.set_visible(False)

    def _update(self):
        if self.useblit:
            super()._update()