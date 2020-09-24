import sys
import threading
import importlib

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QToolBar, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from dragometer.settings import APP_TITLE

from dragometer.components import Plot


def runSumoApp(appPath, api):
    """
    Spawns the SUMO app. It must contain a method called main
    :param appPath: Path to the python module of the SUMO app
    :param api: API instance to be passed to the SUMO app
    """
    module = importlib.import_module(appPath)
    if not hasattr(module, 'main'):
        raise AttributeError('Invalid SUMO app. Method  "main" is required')
    try:
        module.main(api)
    except Exception as e:
        print('Invalid SUMO app.')
        print(e)
        sys.exit(1)


class Dragometer(QMainWindow):
    sAddPlot = pyqtSignal(str)
    sSetSubplots = pyqtSignal(str, int)
    sSetTitle = pyqtSignal(str, str)
    sSetXaxisTitle = pyqtSignal(str, str)
    sSetYaxisTitle = pyqtSignal(str, str)
    sSetXmax = pyqtSignal(str, float)
    sSetYmin = pyqtSignal(str, float)
    sSetYmax = pyqtSignal(str, float)
    sPlot = pyqtSignal(str, float, float, int)

    def __init__(self, appPath):
        super(Dragometer, self).__init__()

        self.setWindowTitle(APP_TITLE)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.screenshot = QAction()
        self.toolbar.addAction(self.screenshot)
        self.screenshot.triggered.connect(self._onScreenshotClicked)
        self.screenshot.setIcon(QIcon.fromTheme("camera-photo"))

        centralWidget = QWidget()
        self.layout = QVBoxLayout()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

        self.plots = dict()

        self.sAddPlot.connect(lambda id_: self._addPlot(id_))
        self.sSetSubplots.connect(lambda id_, *args: self._getPlot(id_).setSubplots(*args))
        self.sSetTitle.connect(lambda id_, *args: self._getPlot(id_).setTitle(*args))
        self.sSetXaxisTitle.connect(lambda id_, *args: self._getPlot(id_).setXaxisTitle(*args))
        self.sSetYaxisTitle.connect(lambda id_, *args: self._getPlot(id_).setYaxisTitle(*args))
        self.sSetXmax.connect(lambda id_, *args: self._getPlot(id_).setXmax(*args))
        self.sSetYmin.connect(lambda id_, *args: self._getPlot(id_).setYmin(*args))
        self.sSetYmax.connect(lambda id_, *args: self._getPlot(id_).setYmax(*args))
        self.sPlot.connect(lambda id_, *args: self._getPlot(id_).plot(*args))

        # Start Sumo
        thread = threading.Thread(target=runSumoApp, args=(appPath, self,))
        thread.setDaemon(True)
        thread.start()

        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _onScreenshotClicked(self):
        for id_, plot in self.plots.items():
            plot.grabScreenshot(id_)

    def _getPlot(self, id_: str) -> Plot:
        if id_ not in self.plots:
            raise KeyError(f'Plot {id_} does not exist.')
        return self.plots[id_]

    @pyqtSlot(str)
    def _addPlot(self, id_: str):
        if id_ in self.plots:
            raise ValueError(f'Plot {id_} already exists.')
        plot = Plot()
        self.plots[id_] = plot
        self.layout.addWidget(plot)

    """ API methods """

    def add_plot(self, id_: str):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        self.sAddPlot.emit(id_)

    def set_subplots(self, id_: str, count: int):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(count) is not int:
            raise TypeError('count must be int')
        if count < 1:
            raise ValueError('count must be >= 1')
        self.sSetSubplots.emit(id_, count)

    def set_title(self, id_: str, title: str):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(title) is not str:
            raise TypeError('title must be string')
        self.sSetTitle.emit(id_, title)

    def set_x_axis_title(self, id_: str, title: str):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(title) is not str:
            raise TypeError('title must be string')
        self.sSetXaxisTitle.emit(id_, title)

    def set_y_axis_title(self, id_: str, title):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(title) is not str:
            raise TypeError('title must be string')
        self.sSetYaxisTitle.emit(id_, title)

    def set_x_max(self, id_: str, xMax: float):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(xMax) is not float and type(xMax) is not int:
            raise TypeError('xMax must be float or int')
        if xMax < 0.:
            raise TypeError('xMax must be >= 0')
        self.sSetXmax.emit(id_, float(xMax))

    def set_y_min(self, id_: str, yMin: float):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(yMin) is not float and type(yMin) is not int:
            raise TypeError('xMax must be float or int')
        self.sSetYmin.emit(id_, float(yMin))

    def set_y_max(self, id_: str, yMax: float):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(yMax) is not float and type(yMax) is not int:
            raise TypeError('xMax must be float or int')
        self.sSetYmax.emit(id_, float(yMax))

    def plot(self, id_: str, x: float, y: float, subplotIndex: int = 0):
        if type(id_) is not str:
            raise TypeError('id_ must be string')
        if type(x) is not float and type(x) is not int:
            raise TypeError('x must be float or int')
        if x < 0:
            raise TypeError('x must be >= 0')
        if type(y) is not float and type(y) is not int:
            raise TypeError('y must be float or int')
        if type(subplotIndex) is not int:
            raise TypeError('subplotIndex must be int')
        if subplotIndex < 0:
            raise TypeError('subplotIndex must be >= 0')
        self.sPlot.emit(id_, float(x), float(y), subplotIndex)
