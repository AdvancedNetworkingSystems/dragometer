from PyQt5.QtCore import Qt, QPointF, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtChart import QChartView, QLineSeries, QChart, QValueAxis

from dragometer.settings import PLOT_WIDTH, PLOT_HEIGHT


class Plot(QChartView):
    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)

        self.setFixedSize(PLOT_WIDTH, PLOT_HEIGHT)

        self.xMax = None
        self.yMin = None
        self.yMax = None

        self.xAutoRescale = True
        self.yMinAutoRescale = True
        self.yMaxAutoRescale = True

        self.seriesList = []

        self.chart = QChart()

        self.xAxis = QValueAxis()
        self.chart.addAxis(self.xAxis, Qt.AlignBottom)

        self.yAxis = QValueAxis()
        self.chart.addAxis(self.yAxis, Qt.AlignLeft)

        self.setSubplots(1)

        self.chart.legend().setVisible(False)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(self.chart)
        # self.setRenderHint(QPainter.Antialiasing)

    def grabScreenshot(self, title):
        pixmap = QPixmap(self.grab())
        pixmap.save(title + '.png', 'PNG')

    @pyqtSlot(int)
    def setSubplots(self, count: int):
        for _ in range(count):
            series = QLineSeries()
            self.chart.addSeries(series)
            series.attachAxis(self.xAxis)
            series.attachAxis(self.yAxis)
            self.seriesList.append(series)

    @pyqtSlot(str)
    def setTitle(self, title: str):
        self.chart.setTitle(title)

    @pyqtSlot(str)
    def setXaxisTitle(self, title: str):
        self.xAxis.setTitleText(title)

    @pyqtSlot(str)
    def setYaxisTitle(self, title: str):
        self.yAxis.setTitleText(title)

    @pyqtSlot(float)
    def setXmax(self, xMax: float):
        self.xAxis.setMax(xMax)
        self.xAutoRescale = False

    @pyqtSlot(float)
    def setYmin(self, yMin: float):
        self.yAxis.setMin(yMin)
        self.yMinAutoRescale = False

    @pyqtSlot(float)
    def setYmax(self, yMax: float):
        self.yAxis.setMax(yMax)
        self.yMaxAutoRescale = False

    @pyqtSlot(float, float, int)
    def plot(self, x: float, y: float, subplotIndex: int):
        if subplotIndex > len(self.seriesList) - 1:
            raise IndexError(f'Invalid subplot index ({subplotIndex}, max: {len(self.seriesList)})')
        if self.xAutoRescale:
            self.xAxis.setMax(x)
        if self.yMinAutoRescale:
            if not self.yMin or y < self.yMin:
                self.yMin = y
                self.yAxis.setMin(y - 0.001)
        if self.yMaxAutoRescale:
            if not self.yMax or y > self.yMax:
                self.yMax = y
                self.yAxis.setMax(y + 0.001)
        self.seriesList[subplotIndex] << QPointF(float(x), float(y))
