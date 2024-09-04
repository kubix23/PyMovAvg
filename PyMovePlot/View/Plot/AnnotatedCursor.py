import numpy as np
from matplotlib import lines
from matplotlib.widgets import Cursor


class AnnotatedCursor(Cursor):

    def __init__(self, data, ax, *, horizOn=..., vertOn=..., useblit=..., **lineprops):
        def onPress(event):
            if event.inaxes != ax: return
            self.press = True

        def onRelease(event):
            self.press = None

        super().__init__(ax, horizOn=horizOn, vertOn=vertOn, useblit=useblit, **lineprops)

        self.x_data = range(data.shape[0])
        self.y_data = data.iloc[:,:-1]
        temp = ["{0}: {{{1}:.2f}}\n".format(self.y_data.keys()[num], num) for num in range(0, len(self.y_data.keys()))]
        self.numberformat = ''.join(temp)
        self.offset = np.array((5, 5))
        self.dataaxis = 'x'
        self.press = None
        self.set_position(0)
        self.text = self.ax.text(
            self.ax.get_xbound()[0],
            self.ax.get_ybound()[0],
            "0, 0",
            animated=bool(self.useblit),
            visible=False)
        self.lastdrawnplotpoint_x = None
        ax.get_figure().canvas.mpl_connect('button_press_event', onPress)
        ax.get_figure().canvas.mpl_connect('button_release_event', onRelease)

    def onmove(self, event):
        if self.press is not None: return

        if self.ignore(event):
            self.lastdrawnplotpoint_x = None
            return

        if not self.canvas.widgetlock.available(self):
            self.lastdrawnplotpoint_x = None
            return

        plotpoint_x = None
        if event.xdata is not None and event.ydata is not None:
            plotpoint_x = self.set_position(event.xdata)
            if plotpoint_x is not None:
                event.xdata = plotpoint_x

        super().onmove(event)

        if not self.get_active() or not self.visible:
            return

        if plotpoint_x is not None:
            temp = [plotpoint_x, event.ydata]
            temp = self.ax.transData.transform(temp)
            temp = temp + self.offset
            temp = self.ax.transData.inverted().transform(temp)
            self.text.set_position(temp)
            self.text.set_text(self.numberformat.format(*self.y_data.values[plotpoint_x]))
            self.text.set_visible(self.visible)
            self.needclear = True
            self.lastdrawnplotpoint_x = plotpoint_x
        else:
            self.text.set_visible(False)

        if self.useblit:
            self.ax.draw_artist(self.text)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()

    def set_position(self, xpos):
        xdata = self.x_data

        if self.dataaxis == 'x':
            pos = xpos
            data = xdata
            lim = self.ax.get_xlim()
        else:
            raise ValueError(f"The data axis specifier {self.dataaxis} should "
                             f"be 'x' or 'y'")

        if pos is not None and lim[0] <= pos <= lim[1]:
            index = np.searchsorted(data, pos)
            if index < 0 or index >= len(data):
                return None
            return xdata[index]

        return None

    def clear(self, event):
        super().clear(event)
        if self.ignore(event):
            return
        self.text.set_visible(False)

    def _update(self):
        if self.useblit:
            super()._update()