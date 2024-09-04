import time

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.widgets import Cursor


class ZoomPan:
    def __init__(self, figure, axes, data=None):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.axes = axes
        self.zoom_factory(axes[0])
        self.pan_factory(axes[0])
        self.bg = [figure.canvas.copy_from_bbox(ax.bbox) for ax in axes]
        self.data = data


    def zoom_factory(self, ax, base_scale=2.):
        def zoom(event):
            if event.inaxes != ax: return
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata
            ydata = event.ydata
            if event.button == 'up':
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                scale_factor = base_scale
            else:
                scale_factor = 1

            if 'ctrl' in event.modifiers:
                new_width = (cur_xlim[1] - cur_xlim[0]) * 1
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            else:
                new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])

            fig.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            fig.canvas.draw_idle()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return

            self.cur_xlim -= event.xdata - self.xpress
            self.cur_ylim -= event.ydata - self.ypress
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            for (axi, bg) in zip(self.axes, self.bg):
                fig.canvas.restore_region(bg)
                for line in axi.lines:
                    ax.draw_artist(line)
                    fig.canvas.blit(ax.bbox)
            fig.canvas.flush_events()

        def clear(event):
            self.bg = [fig.canvas.copy_from_bbox(axi.bbox) for axi in self.axes]

        fig = ax.get_figure()  # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)
        fig.canvas.mpl_connect('draw_event', clear)

        # return the function
        return onMotion