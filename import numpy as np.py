import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class CustomAxis(pg.AxisItem):
    @property
    def nudge(self):
        if not hasattr(self, "_nudge"):
            self._nudge = 5
        return self._nudge

    @nudge.setter
    def nudge(self, nudge):
        self._nudge = nudge
        s = self.size()
        # call resizeEvent indirectly
        self.resize(s + QtCore.QSizeF(1, 1))
        self.resize(s)

    def resizeEvent(self, ev=None):
        # s = self.size()

        ## Set the position of the label
        nudge = self.nudge
        br = self.label.boundingRect()
        p = QtCore.QPointF(0, 0)
        if self.orientation == "left":
            p.setY(int(self.size().height() / 2 + br.width() / 2))
            p.setX(-nudge)
        elif self.orientation == "right":
            p.setY(int(self.size().height() / 2 + br.width() / 2))
            p.setX(int(self.size().width() - br.height() + nudge))
        elif self.orientation == "top":
            p.setY(-nudge)
            p.setX(int(self.size().width() / 2.0 - br.width() / 2.0))
        elif self.orientation == "bottom":
            p.setX(int(self.size().width() / 2.0 - br.width() / 2.0))
            p.setY(int(self.size().height() - br.height() + nudge))
        self.label.setPos(p)
        self.picture = None


app = QtGui.QApplication([])

x = np.linspace(0, 1, 10000)
y = np.linspace(350, 2500, 10000)


win = pg.GraphicsWindow()
plot = win.addPlot(
    x=x, y=y, title="Plot", axisItems={"bottom": CustomAxis(orientation="bottom")}
)

label_style = {"color": "#EEE", "font-size": "14pt"}
plot.setLabel("bottom", "some x axis label", **label_style)
plot.setLabel("left", "some y axis label")
plot.getAxis("left").setLabel(**label_style)
font = QtGui.QFont()
font.setPixelSize(14)
plot.getAxis("bottom").tickFont = font
plot.getAxis("bottom").setStyle(tickTextOffset=50)

plot.getAxis("left").tickFont = font
plot.getAxis("left").setStyle(tickTextOffset=14)


def on_timeout():
    plot.getAxis("bottom").nudge += 1

timer = QtCore.QTimer(timeout=on_timeout, interval=500)
timer.start() 

if __name__ == "__main__":
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
        QtGui.QApplication.instance().exec()